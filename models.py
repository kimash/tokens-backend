# mongoengine database module
from mongoengine import *
from flask.ext.mongoengine.wtf import model_form

from datetime import datetime
import logging

class Token(Document):
	name = StringField(max_length=120) # token name

class TokenVal(EmbeddedDocument):
	tokenName = ListField( ReferenceField(Token) ) # token name
	yesVal = IntField(min_value=-5, max_value=5)	# number of tokens for yes
	noVal = IntField(min_value=-5, max_value=5)	# number of tokens for no

class Question(EmbeddedDocument):
	qText = StringField(max_length=120)	# question to ask
	tokenVals = ListField( EmbeddedDocumentField(TokenVal) )	# list of affected tokens
	
class Round(Document):
	title = StringField(max_length=120)	# give the round a title
	slug = StringField()	# slug for URL
	questions = ListField( EmbeddedDocumentField(Question) )	# list of questions
	tokens = ListField( ReferenceField(Token) ) # allows users to specify tokens for round

# Validation Form for above data
RoundForm = model_form(Round)
TokenForm = model_form(Token)










