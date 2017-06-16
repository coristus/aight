from e5 import app, event_stream, user_store, portal, context_store

from e5.auth import User

from teamX import *

from flask import Blueprint

blueprint = Blueprint(
    'hr analytics',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/pi')

app.register_blueprint(blueprint)

portal.title = "HR Analytics Lab"
portal.logo = "/static/pi/logo.png"


## ALGEMENE PANELS
##

### MISC mockups
##


app.run(host='0.0.0.0')
#- cache content en tijd aware
