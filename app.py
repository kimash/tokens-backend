import os, datetime
import re
from flask import Flask, request, render_template, redirect, abort, flash, json

from unidecode import unidecode

# mongoengine database module
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'tokensGame'}
app.logger.debug("Connecting to MongoLabs")
db = MongoEngine(app) # connect MongoEngine with Flask App

# import data models
import models


# --------- Routes ----------
# this is our main pagex
@app.route("/", methods=['GET','POST'])
def index():

	round_form = models.RoundForm(request.form)

	# if form was submitted and it is valid...
	if request.method == "POST" and round_form.validate():
	
		# create new round
		round = models.Round()
		round.title = request.form.get('title','no title')
		round.numQ = request.form.get('number of questions')
		round.slug = slugify(round.title)
		round.maxTokens = 0
		
		round.save() # save it

		# redirect to the new round page
		return redirect('/rounds/%s' % round.title)

	else:

		# for form management, checkboxes are weird (in wtforms)
		# prepare checklist items for form
		# you'll need to take the form checkboxes submitted
		# and idea_form.categories list needs to be populated.
		#if request.method=="POST" and request.form.getlist('categories'):
			#for c in request.form.getlist('categories'):
				#idea_form.categories.append_entry(c)


		# render the template
		templateData = {
			'rounds' : models.Round.objects(),
			'title' : title,
			'form' : round_form
		}
		
		# app.logger.debug(templateData)

		return render_template("main.html", **templateData)


@app.route("/rounds/<round_slug>")
def round_display(round_slug):

	# get round by round_slug
	try:
		roundsList = models.Round.objects(slug=round_slug)
	except:
		abort(404)

	# prepare template data
	templateData = {
		'round' : roundsList[0]
	}

	# render and return the template
	return render_template('idea_entry.html', **templateData)

@app.route("/rounds/edit/<round_id>", methods=['GET','POST'])
def round_edit(round_id):

	if request.method == 'POST':
		try:
			idea = models.Round.objects.get(id=round_id)
		except:
			abort(404)

		# populate the RoundForm with incoming form data
		roundForm = models.RoundForm(request.form)

		if ideaForm.validate():
			updateData = {
				'set__title' : request.form.get('title'),
				'set__numQ' : request.form.get('number of questions'),
			}
			idea.update(**updateData) # update the idea
			
			# flash message
			flash('Round updated')

			# redirect to the GET method of the current page
			return redirect('/rounds/edit/%s' % round.id )

		else:

			# error display form with errors
			templateData = {
				'round_id' : round.id,
				'form' : roundForm
			}

			return render_template('idea_edit.html', **templateData)

	else:
		# get the round convert it to the model form, this prepopulates the form
		try:
			round = models.Round.objects.get(id=round_id)
			roundForm = models.RoundForm(obj=round)

		except:
			abort(404)

		templateData = {
			'round_id' : round.id,
			'form' : roundForm
		}

		return render_template('idea_edit.html', **templateData)


@app.route("/rounds/<round_id>/questions", methods=['POST'])
def round_questions(round_id):

	#for n in range(round.numQ):
	qText = request.form.get('qText')
	yesTokens = request.form.get('0 to 5')
	noTokens = request.form.get('0 to 5')

	if question == '' or yesTokens == '' or noTokens == '':
		# no name or comment, return to page
		return redirect(request.referrer)


	#get the round by id
	try:
		idea = models.Round.objects.get(id=round_id)
	except:
		# error, return to where you came from
		return redirect(request.referrer)


	# create questions
	yCount = 0
	
	for n in range(round.numQ):
		question[n] = models.Question()
		question[n].qText = request.form.get('qText')
		question[n].yesTokens = request.form.get('0 to 5')
		question[n].noTokens = request.form.get('0 to 5')			
		# append comment to idea
		round.questions.append(question[n])
		yCount += question[n].yesTokens
		
	round.maxTokens = yCount

	# save it
	round.save()

	return redirect('/rounds/%s' % round.slug)


from flask import jsonify


@app.route('/data/rounds')
def data_rounds():

	# query for the ideas
	rounds = models.Round.objects().limit(20)

	if rounds:

		# list to hold ideas
		public_rounds = []

		#prep data for json
		for r in rounds:
			tmpRound = roundToDict(r)
			
			# insert idea dictionary into public_ideas list
			public_rounds.append( tmpRound )

		# prepare dictionary for JSON return
		data = {
			'status' : 'OK',
			'rounds' : public_rounds
		}

		# jsonify (imported from Flask above)
		# will convert 'data' dictionary and set mime type to 'application/json'
		return jsonify(data)

	else:
		error = {
			'status' : 'error',
			'msg' : 'unable to retrieve ideas'
		}
		return jsonify(error)

@app.route('/data/rounds/<id>')
def data_round(id):
		

	# query for the ideas - return oldest first, limit 10
	try:
		round = models.Round.objects.get(id=id)
		if round:
			tmpRound = roundToDict(round)
			
			# prepare dictionary for JSON return
			data = {
				'status' : 'OK',
				'round' : tmpRound
			}

			# jsonify (imported from Flask above)
			# will convert 'data' dictionary and set mime type to 'application/json'
			return jsonify(data)

	except:
		error = {
			'status' : 'error',
			'msg' : 'unable to retrieve ideas'
		}
		return jsonify(error)




@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def roundToDict(round):
	# create a dictionary
	tmpRound = {
		'id' : str(round.id),
		'title' : round.title,
		'numQ' : round.numQ,
		'maxTokens' : round.maxTokens
	}

	# questions - embedded documents
	tmpRound['questions'] = [] # list - will hold all comment dictionaries
	
	# loop through round questions
	for q in round.questions:
		question_dict = {
			'text' : q.qText,
			'yesTokens' : q.yesTokens,
			'noTokens' : q.noTokens
		}

		# append comment_dict to ['comments']
		tmpRound['questions'].append(question_dict)

	return tmpRound


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))



# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	