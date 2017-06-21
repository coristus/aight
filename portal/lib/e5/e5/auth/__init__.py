import os
import base64
import onetimepass
import StringIO
import pyqrcode

import inflection

from e5 import app, portal, login_manager
from bson.objectid import ObjectId

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask import request, render_template, redirect, flash, url_for, Markup
from flask_login import UserMixin, login_required, current_user, login_user, logout_user, fresh_login_required

@login_manager.user_loader
def load_user(user_id):
    u = app.config['USER_COLLECTION'].find_one({"_id": ObjectId(user_id)})
    if not u:
        return None
    return User(u['_id'], u['username'], u['fullname'], u['otp_secret'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print "RENDERING LOGIN ON GET"
        return render_template('e5login.html', css=portal.css, logo=portal.logo, title=portal.title)
    username = request.form['username']
    password = request.form['password']
    token = request.form['token']

    remember = False
    if 'remember' in request.form:
        remember = True

    user = app.config['USER_COLLECTION'].find_one({"username": username.lower()})
    if user == None:
        flash("Wrong login credentials", category='danger')
        print "USER NOT FOUND ERROR"
        return render_template('e5login.html', css=portal.css, logo=portal.logo, title=portal.title)

    user_obj = User(user['_id'], user['username'], user['fullname'], user['otp_secret'])
    if user_obj.otp_secret != '' and not user_obj.verify_totp(token):
        flash("Wrong login credentials", category='danger')
        print "TOKEN ERROR"
        return render_template('e5login.html', css=portal.css, logo=portal.logo, title=portal.title)


    if user and User.validate_login(user['password'], password):
        login_user(user_obj, remember=remember)
        # flash("Logged in successfully", category='success')
        if user['otp_secret'] == '':
            flash(Markup("<strong>Belangrijk!</strong> U heeft two factor authenticatie nog niet ingeschakeld. Ga naar uw <a href='/account'>account instellingen</a> om dat alsnog te doen."), "warning")
        print "LOGIN SUCCESS"
        return redirect(request.args.get("next") or url_for("renderIndex"))
    flash("Wrong login credentials", category='danger')
    print "LOGIN ERROR"
    return render_template('e5login.html', css=portal.css, logo=portal.logo, title=portal.title)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account')
@fresh_login_required
def acount():
    return render_template('e5account.html', css=portal.css, logo=portal.logo, title=portal.title)

@app.route('/changepassword', methods=['POST'])
@fresh_login_required
def change_password():
    oldpassword  = request.form['oldpassword']
    newpassword  = request.form['newpassword']
    newpassword2 = request.form['newpassword2']

    pass_hash = generate_password_hash(newpassword, method='pbkdf2:sha256')

    user = app.config['USER_COLLECTION'].find_one({"_id": ObjectId(current_user.get_id())})

    if not User.validate_login(user['password'], oldpassword):
        flash('Het door u opgegeven oude wachtwoord klopt niet', 'danger')
        return redirect(url_for('acount'))
    if not newpassword == newpassword2:
        flash('De door u opgegeven nieuwe wachtwoorden zijn niet hetzelfde', 'danger')
        return redirect(url_for('acount'))

    app.config['USER_COLLECTION'].update_one(
        {'_id': current_user.get_id()}, { '$set':  {'password': pass_hash}}
    )
    flash('Uw wachtwoord is succesvol aangepast', 'success')
    return redirect(url_for('acount'))


@app.route('/enable2fa')
@fresh_login_required
def enable2FA():
    current_user.generate_secret()

    app.config['USER_COLLECTION'].update_one(
        {'_id': current_user.get_id()}, { '$set':  {'otp_secret': current_user.otp_secret}}
    )

    return redirect(url_for('acount'))

@app.route('/disable2fa')
@fresh_login_required
def disable2FA():
    current_user.generate_secret()

    app.config['USER_COLLECTION'].update_one(
        {'_id': current_user.get_id()}, { '$set':  {'otp_secret': ''}}
    )

    return redirect(url_for('acount'))

@app.route('/qrcode')
@fresh_login_required
def qrcode():
    # render qrcode for FreeTOTP
    url = pyqrcode.create(current_user.get_totp_uri())
    stream = StringIO.StringIO()
    url.svg(stream, scale=5)
    return stream.getvalue().encode('utf-8'), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

class User(UserMixin):

    def __init__(self, id, username, fullname, otp_secret):
        self._id = id
        self.username = username
        self.fullname = fullname
        # for FlaskJWT purposes...
        self.otp_secret = otp_secret

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    @property
    def id(self):
        return str(self._id)

    def generate_secret(self):
        self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    def get_totp_uri(self):
        return 'otpauth://totp/{0}:{1}?secret={2}&issuer={0}' \
            .format(inflection.parameterize(unicode(portal.title), separator='-'), self.username, self.otp_secret)

    def verify_totp(self, token):
        return onetimepass.valid_totp(token, self.otp_secret)

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)
