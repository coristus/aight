import abc
from flask import session, request, render_template, abort, redirect

## Manager
class Portal(object):

    ## CONFIG STATE
    panels = []
    enabledPanels = {}

    forms = []
    formsByID = {}

    algorithmsMap = {}
    algorithms = []

    def __init__(self, title="E5 Portal", css="/static/e5/e5.css",  logo="/static/logo.png"):
        self._title = title
        self._css = css
        self._logo = logo

    @property
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, value):
        self._logo = value

    @property
    def css(self):
        return self._css

    @css.setter
    def css(self, value):
        self._css = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def registerAlgorithm(self, algorithm):
        self.algorithmsMap[algorithm.getId()] = algorithm
        self.algorithms.append(algorithm)

    def registerPanel(self, panel):
        self.panels.append(panel)

    def isEnabled(self, id):
        return True if id not in self.enabledPanels or self.enabledPanels[id] is True else False

    def enable(self, id):
        self.enabledPanels[id] = True

    def disable(self, id):
        self.enabledPanels[id] = False

    def renderIndex(self):
        return self.renderPanel(None)

    def renderPanel(self, panel_id):
        ## retrieve topic list from session
        try:
            topics = session['topics']
        except KeyError:
            ## initialize if it didn't exist
            topics = []
            topics.append(Topic("Home", "home", None))
            session['topics'] = topics

        ## clear the topic list if clear argument is passed
        if request.args.get('clear') is not None:
            topics = []
            topics.append(Topic("Home", "home", None))
            session['topics'] = topics

        if request.args.get('topic') is not None:
            index = int(request.args.get('topic')) + 1
            if index > 0:
                topics = topics[0:index]
                session['topics'] = topics

        ## UPDATE THE PANEL THAT WAS ADDRESSED IN THE ROUTE /panel-id
        if panel_id is not None:
            for panel in self.panels:
                if panel.id() == panel_id:
                    panel.update(request, topics)
                    session['topics'] = topics
                    break
            else:
                abort(404)

        ## establish visible panels...
        mainpanels = []
        rightpanels = []
        menupanels = []
        state = {}
        for panel in self.panels:
            if panel.applies(topics):
                state[panel.id()] = panel.getTemplateData(topics)
                if panel.mode(topics) == "main" and self.isEnabled(panel.id()):
                    mainpanels.append(panel)
                if panel.mode(topics) == "right" and self.isEnabled(panel.id()):
                    rightpanels.append(panel)
                if panel.mode(topics) == "menu" and self.isEnabled(panel.id()):
                    menupanels.append(panel)

        return render_template('e5portal.html', css=self._css, title=self._title, logo=self._logo, state=state, topics=topics, menupanels=menupanels, mainpanels=mainpanels, rightpanels=rightpanels, getTemplate=lambda x:  x.getTemplate())

    def renderResource(self, panel_id, resource_uri):
        try:
            topics = session['topics']
        except KeyError:
            ## initialize if it didn't exist
            topics = []
            topics.append(Topic("Home", "home", None))
            session['topics'] = topics

        for panel in self.panels:
            if panel.id() == panel_id:
                return panel.renderResource(resource_uri, topics=topics)
        abort(404)

    def registerForm(self, f):
        self.formsByID[f.id] = f
        self.forms.append(f)

    def renderForm(self, form_id, requestData, user):
        try:
            topics = session['topics']
        except KeyError:
            ## initialize if it didn't exist
            topics = []
            topics.append(Topic("Home", "home", None))
            session['topics'] = topics

        form = self.formsByID[form_id]
        if form is None:
            return
        if 'formdata.'+form_id in session:
            formdata = session['formdata.'+form_id]
        else:
            formdata = {}
            session['formdata.'+form_id] = {}

        form.update(formdata, requestData)
        session['formdata.'+form_id] = formdata

        if not form.validate(formdata):
            return render_template(form.getFormUri(), css=self._css, title=self._title, logo=self._logo, topics=topics, form=form, formdata=formdata)
        else:
            submit_handlers = form.get_submit_handlers()

            for submit_handler in submit_handlers:
                submit_handler.handle(topics[-1], form_id, formdata, user)

            session['formdata.'+form_id] = {}
            return redirect(form.getSuccesUri())

class Topic(dict):
    def __init__(self, topic, kind, d):
        self['topic'] = topic
        self['kind'] = kind
        if d is not None:
            self.update(d)

## Contract
class Panel:
    def id(self):
        return
    def mode(self, topics):
        return "main"
    def applies(self, topics):
        return
    def update(self, request, topics):
        return
    def getTemplateData(self, topics):
        return
    def getTemplate(self):
        return ""
    ## Method for rendering separate resources, such as images and charts?
    def renderResources(self, uri, topics=[]):
        return
    def topicOfKind(self, topics, kind):
        return topics[len(topics)-1]['kind'] == kind

## Base
class BasePanel(Panel):
    def __init__(self, panelID, template, topicKind, panelType):
        self.panelID = panelID
        self.template = template
        self.topicKind = topicKind
        self.panelType = panelType
    def id(self):
        return self.panelID
    def mode(self, topics):
        return self.panelType
    def applies(self, topics):
        return self.topicOfKind(topics, self.topicKind)
    def topicOfKind(self, topics, kind):
        return topics[len(topics)-1]['kind'] == kind




## Contract
class Form:
    def __init__(self, id,label, succesUri="/index", formUri="e5form.html", elements=[], submit_handlers=[]):
        self.label = label
        self.id = id
        self.succesUri = succesUri
        self.formUri = formUri
        self.elements = elements
        self.submit_handlers = submit_handlers

    def getSuccesUri(self):
        return self.succesUri

    def getFormUri(self):
        return self.formUri

    def addFormElement(self, element):
        self.elements.append(element)

    def update(self, formdata, requestData):
        for elt in self.elements:
            elt.update(formdata, requestData)

    def validate(self, formdata):
        valid = True
        for elt in self.elements:
            valid = valid and elt.validate(formdata)
        return valid

    def get_submit_handlers(self):
        return self.submit_handlers


class SubmitHandler(object):
    ''' Submit handler interface '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle(self, topic, form_id, form_data):
        ''' handle submitted form data'''
        raise NotImplementedError('This should be implemented by subclass')


## Contract
class FormElement:
    def update(self, formData, requestData):
        pass
    def validate(self, formData):
        pass
    def getTemplate(self):
        pass

class BaseReadOnlyField(FormElement):
    def update(self, formdata, requestData):
        pass
    def validate(self, formdata):
        return True


## Base
class BaseField(FormElement):

    def __init__(self, id, label, mandatory, popuptext=''):
        self.id = id
        self.label = label
        self.mandatory = mandatory
        self.popuptext = popuptext

    def update(self, formdata, requestData):
        if self.id in requestData:
            formdata[self.id] = requestData[self.id]

    def validate(self, formdata):
        if self.mandatory and self.id  not in formdata:
            return False
        if self.mandatory and self.id in formdata:
            return formdata[self.id] != None and len(formdata[self.id]) > 0
        return True
