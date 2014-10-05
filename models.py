# mongoengine database module
from mongoengine import *
from flask.ext.mongoengine.wtf import model_form

from datetime import datetime
import logging

class Question(EmbeddedDocument):
	qText = StringField(max_length=120, required=True)	# question to ask
	yesTokens = IntField(min_value=0, max_value=5, required=True)	# yes token value
	noTokens = IntField(min_value=0, max_value=5, required=True)	# no token value
	
class Round(Document):
	title = StringField(max_length=120)	# give the round a title
	numQ = IntField(min_value=1, max_value=5)	# number of questions in round
	questions = ListField( EmbeddedDocumentField(Question) )	# list of questions
	slug = StringField()	# slug for URL
	
	# total number of yes tokens above, i.e. max number of tokens for game
	maxTokens = IntField()
	
	# for int y in EmbeddedDocumentField(yesTokens)

# Validation Form for above data
RoundForm = model_form(Round)
#QForm = model_form(Question)










