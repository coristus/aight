## Default
##class ChecklistElement


## Portal API
from flask import Flask, session, request, Response, render_template, make_response, abort, _app_ctx_stack, redirect
from flask.views import View

import sys

from e5.events.event_stream import EventStream
from e5.portal import *


class FormHeader(BaseReadOnlyField):
    def __init__(self, header, introduction=""):
        self.header=header
        self.introduction = introduction
    def getTemplate(self):
        return "formelements/e5formheader.html"

class FormMessage(BaseReadOnlyField):
    def __init__(self, message):
        self.message = message

    def getTemplate(self):
        return "formelements/e5formmessage.html"


class TextField(BaseField):
    def getTemplate(self):
        return "formelements/e5textfield.html"

class NumberField(BaseField):
    def getTemplate(self):
        return "formelements/e5numberfield.html"
    
class NumberSliderField(BaseField):
    def __init__(self, id, label, mandatory, popuptext='', min_value=30, max_value=70, step=1):
        self.id = id
        self.label = label
        self.mandatory = mandatory
        self.popuptext = popuptext
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

    def getTemplate(self):
        return "formelements/e5numbersliderfield.html"

class DateField(BaseField):
    def getTemplate(self):
        return "formelements/e5datefield.html"

class TextareaField(BaseField):
    def getTemplate(self):
        return "formelements/e5textareafield.html"

class ChoiceField(BaseField):
    def __init__(self, id, label, mandatory, choices, popuptext=''):
        self.id = id
        self.label = label
        self.mandatory = mandatory
        self.choices = choices
        self.popuptext = popuptext

    def validate(self, formdata):
        if self.mandatory and self.id  not in formdata:
            return False
        if self.mandatory and self.id in formdata:
            return formdata[self.id] != None and formdata[self.id] in self.choices
        return True

    def getTemplate(self):
        return "formelements/e5choicefield.html"


class Instruction(BaseField):
    def __init__(self, id, label, instruction, confirmation="Dat is gebeurd"):
        self.id = id
        self.label = label
        self.instruction = instruction
        self.confirmation= confirmation
        self.mandatory = True

    def getTemplate(self):
        return "formelements/e5instruction.html"

class OptionalFields(BaseField):
    def __init__(self, elements, condition):
        self._elements = elements
        self._condition = condition

    def update(self, formdata, requestData):
        #TODO only update if condition is true?
        for e in self._elements:
            e.update(formdata, requestData)

    def getTemplate(self):
        return "formelements/e5optionalfields.html"



class Derivation:
    def derive(self, formdata, user=None):
        pass

class CopyDerivation(Derivation):
    def __init__(self, source):
        self._source = source

    def derive(self, formdata):
        if self._source in formdata:
            return formdata[self._source]
        else:
            return None
class ConstantDerivation(Derivation):
    def __init__(self, constant):
        self._constant = constant

    def derive(self, formdata):
            return self._constant

class DerivedField(BaseField):
    def __init__(self, id, derivation):
        self._id = id
        self._derivation = derivation

    def update(self, formdata, requestData):
        val = self._derivation.derive(formdata)
        if val != None:
            formdata[self._id] = val
    def validate(self, formdata):
        return True

    def getTemplate(self):
        return "formelements/e5derivedfield.html"
