from e5 import portal, event_stream, context_store
from e5.portal.panels import AllFormsPanel
from e5.portal.formelements import *
from e5.portal.submit_handlers import *

portal.registerForm(
    Form("test", "Assessment en Test", elements=[
        FormHeader("iNstabiliteit", "Hier komen de vragen over de instabiliteit..."),
        NumberSliderField("N", "iNstabiliteit", True),
        NumberSliderField("TTN1", "Gevoeligheid", True),
        NumberSliderField("TTN2", "Intensiteit", True),
        NumberSliderField("TTN3", "Interpretatie", True),
        NumberSliderField("TTN4", "Hersteltijd", True),
        NumberSliderField("TTN5", "Terughoudendheid", True),
        FormHeader("Extravertie", "Hier komen de vragen over de extravertie..."),
        NumberSliderField("E", "Extravertie", True),
        NumberSliderField("TTE1", "Enthousiasme", True),
        NumberSliderField("TTE2", "Sociabiliteit", True),
        NumberSliderField("TTE3", "Energie", True),
        NumberSliderField("TTE4", "Leiding nemen", True),
        NumberSliderField("TTE5", "Directheid", True),
        FormHeader("Openstaan", "Hier komen de vragen over openstaan..."),
        NumberSliderField("O", "Openstaan", True),
        NumberSliderField("TTO1", "Verbeelding", True),
        NumberSliderField("TTO2", "Complexiteit", True),
        NumberSliderField("TTO3", "Veranderingen", True),
        NumberSliderField("TTO4", "Autonomie", True),
        FormHeader("Aanpassen", "Hier komen de vragen over aanpassen..."),
        NumberSliderField("A", "Aanpassen", True),
        NumberSliderField("TTA1", "Service", True),
        NumberSliderField("TTA2", "Overeenstemming", True),
        NumberSliderField("TTA3", "Erkenning", True),
        NumberSliderField("TTA4", "Vertrouwen", True),
        NumberSliderField("TTA5", "Tact", True),
        FormHeader("Conscientieusheid", "Hier komen de vragen over de conscientieusheid..."),
        NumberSliderField("C", "Conscientieusheid", True),
        NumberSliderField("TTC1", "Perfectionisme", True),
        NumberSliderField("TTC2", "Organisatie", True),
        NumberSliderField("TTC3", "Gedrevenheid", True),
        NumberSliderField("TTC4", "Concentratie", True),
        NumberSliderField("TTC5", "Methodisch werken", True),
        DateField("datum", "Testdatum", True)
    ], submit_handlers=[EventStoreHandler(event_stream, "Assessment en Test", 'geteste', submit_date_field="datum")]))

portal.registerForm(
    Form("extendedTest", "Drijfveren en Intelligentie", elements=[
        FormHeader("iNstabiliteit", "Hier komen de vragen over de instabiliteit..."),
        NumberSliderField("TTN1", "Gevoeligheid", True),
        NumberSliderField("TTN2", "Intensiteit", True),
        NumberSliderField("TTN3", "Interpretatie", True),
        NumberSliderField("TTN4", "Hersteltijd", True),
        NumberSliderField("TTN5", "Terughoudendheid", True),
        FormHeader("Extravertie", "Hier komen de vragen over de extravertie..."),
        NumberSliderField("TTE1", "Enthousiasme", True),
        NumberSliderField("TTE2", "Sociabiliteit", True),
        NumberSliderField("TTE3", "Energie", True),
        NumberSliderField("TTE4", "Leiding nemen", True),
        NumberSliderField("TTE5", "Directheid", True),
        FormHeader("Openstaan", "Hier komen de vragen over openstaan..."),
        NumberSliderField("TTO1", "Verbeelding", True),
        NumberSliderField("TTO2", "Complexiteit", True),
        NumberSliderField("TTO3", "Veranderingen", True),
        NumberSliderField("TTO4", "Autonomie", True),
        FormHeader("Aanpassen", "Hier komen de vragen over aanpassen..."),
        NumberSliderField("TTA1", "Service", True),
        NumberSliderField("TTA2", "Overeenstemming", True),
        NumberSliderField("TTA3", "Erkenning", True),
        NumberSliderField("TTA4", "Vertrouwen", True),
        NumberSliderField("TTA5", "Tact", True),
        FormHeader("Conscientieusheid", "Hier komen de vragen over de conscientieusheid..."),
        NumberSliderField("TTC1", "Perfectionisme", True),
        NumberSliderField("TTC2", "Organisatie", True),
        NumberSliderField("TTC3", "Gedrevenheid", True),
        NumberSliderField("TTC4", "Concentratie", True),
        NumberSliderField("TTC5", "Methodisch werken", True),
        FormHeader("Profileren", "Hier komen de vragen over profileren..."),
        NumberSliderField("T_Invloed", "Invloed", True),
        NumberSliderField("T_Prestatie", "Prestatie", True),
        NumberSliderField("T_Welvaart", "Welvaart", True),
        FormHeader("Beleven", "Hier komen de vragen over beleven..."),
        NumberSliderField("T_Plezier", "Plezier", True),
        NumberSliderField("T_Avontuur", "Avontuur", True),
        NumberSliderField("T_Vrijheid", "Vrijheid", True),
        FormHeader("Verbinden", "Hier komen de vragen over verbinden..."),
        NumberSliderField("T_Dialoog", "Dialoog", True),
        NumberSliderField("T_Zorg", "Zorg", True),
        NumberSliderField("T_Team", "Team", True),
        FormHeader("Behouden", "Hier komen de vragen over behouden..."),
        NumberSliderField("T_Rechtvaardigheid", "Rechtvaardigheid", True),
        NumberSliderField("T_Traditie", "Tradite", True),
        NumberSliderField("T_Zekerheid", "Zekerheid", True),
        FormHeader("Intelligentie", "Dit is de vraag over uw intelligentie..."),
        NumberSliderField("Tscore_BA", "T-score Bachelor", True),
        DateField("datum", "Testdatum", True)
    ], submit_handlers=[EventStoreHandler(event_stream, "Drijfveren en Intelligentie", 'geteste', submit_date_field="datum")]))

portal.registerForm(
    Form("createmedewerkercontext", "Nieuwe medewerker", elements=[
        TextField("naam", "Volledige naam", True),
        TextField("team", "Afdeling", True)
    ], submit_handlers=[ContextStoreHandler(context_store, "medewerker")]))

kind_map = {
    'home': ["createmedewerkercontext"],
    'user': ["test", "extendedTest"]
}

portal.registerPanel(AllFormsPanel("forms", "home", "right", portal.forms, kind_map))
portal.registerPanel(AllFormsPanel("forms", "user", "right", portal.forms, kind_map))