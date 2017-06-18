from e5 import app, event_stream, user_store, portal, context_store

from e5.auth import User
from e5.portal.panels import ContextListPanel, EventsPanel
from e5.data import PandasDataService

from forms import *
from team2 import *
from competence import CompetenceDevelopmentScoringAlgorithm, CompetencePrediction, CompetenceAlgorithmProjection

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


employees_context_panel_home = ContextListPanel(event_stream, "medewerker", "medewerkers", "naam", "user", "home", "main", "medewerkers")
portal.registerPanel(employees_context_panel_home)

portal.registerPanel(EventsPanel("timeline", "user", "main", event_stream, details="timeline-details.html"))

### COMPETENTIE VOORSPELLER PANELEN EN ALGO's
##
facets = ['TTN1', 'TTN2', 'TTN3', 'TTN4', 'TTN5',
  'TTE1', 'TTE2', 'TTE3', 'TTE4', 'TTE5',
  'TTO1', 'TTO2', 'TTO3', 'TTO4',
  'TTA1', 'TTA2', 'TTA3', 'TTA4', 'TTA5',
  'TTC1', 'TTC2', 'TTC3', 'TTC4', 'TTC5']

competences_data = PandasDataService("../data/lab1/Ontwikkelbaarheid competenties.csv", ",", None)

compentence_predictor = CompetenceDevelopmentScoringAlgorithm('Ontwikkelbaarheidsvoorspeller')
compentence_predictor.configure({'cutOff': 2, 'trainingData': competences_data})
portal.registerAlgorithm(compentence_predictor)

compentence_algorithm_projection = CompetenceAlgorithmProjection("competenceVoorspellerProjection", facets, compentence_predictor)
event_stream.register_projection(compentence_algorithm_projection)

portal.registerPanel(CompetencePrediction(event_stream, compentence_algorithm_projection))

### Team 2
# Register your code here. For an example, see part above

app.run(host='0.0.0.0')
#- cache content en tijd aware
