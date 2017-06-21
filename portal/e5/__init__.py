import inflection

from flask import Flask, Blueprint, _app_ctx_stack
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = (
    "Voor deze pagina vragen we u voor de veiligheid opnieuw in te loggen."
)
login_manager.needs_refresh_message_category = "warning"

blueprint = Blueprint(
    'e5',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path=app.static_url_path + '/e5')

app.register_blueprint(blueprint)

from e5.portal import Portal

portal = Portal()

from e5.portal import routes

from e5.events.event_store import MongoEventStore
from e5.events.event_stream import EventStream

event_store = MongoEventStore(app.config['EVENTS_COLLECTION'])

from e5.events.context_store import MongoContextStore
context_store = MongoContextStore(app.config['CONTEXTS_COLLECTION'])

from e5.events.user_store import MongoUserStore
user_store = MongoUserStore(app.config['USER_COLLECTION'])

event_stream = EventStream()
event_stream.register_event_store(event_store)
event_stream.register_context_store(context_store)

from e5.events import routes

@app.template_filter('humanize')
def humanize(arg):
    return inflection.humanize(inflection.underscore(arg))

class ConfigurationException(Exception):

    def __init__(self, message):
        self.message = message

    def getMessage(self):
        return self.message
