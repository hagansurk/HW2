## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json
#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################
class Artistform(FlaskForm):
	artist = StringField('Enter Artist Name Here: ', validators = [Required()])
	submit = SubmitField('Submit')

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album: ', validators=[Required()])
	like_ness = RadioField('How much do you like this album? (1 low, 3 high', validators = [Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artist_form():
	artistForm = Artistform()
	return render_template('artistform.html', form=artistForm)

@app.route('/artistinfo', methods = ['GET'])
def artist_info():
	re = requests.get("https://itunes.apple.com/search?", params = {'term':request.args.get('artist')}).json()
	return render_template('artist_info.html', objects = re['results'])

@app.route('/artistlinks')
def link_art():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>', methods = ['POST', 'GET'])
def spec_art(artist_name):
	artist = request.args.get(artist_name)
	re = requests.get("https://itunes.apple.com/search?", params = {'term':artist_name}).json()
	print(re)
	return render_template('specific_artist.html', results = re['results'])

@app.route('/album_entry')
def alb_ent():
	alb_form = AlbumEntryForm()
	return render_template('album_entry.html', form= alb_form)

@app.route('/album_result')
def alb_res():
	alb_form = AlbumEntryForm(request.form)
	if request.method == 'GET' and alb_form.validate_on_submit():
		album = alb_form.album_name.data
		like = alb_form.like_ness.data
		return render_template('album_data.html', album_enter=album, likeness = like)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
