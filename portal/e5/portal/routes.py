from e5 import app, portal

from flask import request
from flask_login import login_required, fresh_login_required, current_user

@app.route('/')
@app.route('/index')
@login_required
def renderIndex():
    return portal.renderIndex()

@app.route('/panel/<panel_id>')
@login_required
def renderPanel(panel_id):
    return portal.renderPanel(panel_id)

@app.route('/panel/<panel_id>/<resource_uri>')
@login_required
def renderResource(panel_id, resource_uri):
    return portal.renderResource(panel_id, resource_uri)

@app.route('/form/<form_id>')
@fresh_login_required
def renderForm(form_id):
    return portal.renderForm(form_id, request.args, current_user)