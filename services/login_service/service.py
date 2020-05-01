# -*- coding: utf-8 -*-
import flask 						as flask
import flask_wtf 					as wtf
import flask_login 					as flogin
from flask_login 					import current_user, login_user
import os 							as os
from static.modules.config 			import Config, Courier
from static.modules.alchemy.users 	import User
from static.modules.alchemy.jobs  	import Jobs


from static.modules.alchemy 		import session as Session

""" Service User"""

folder = "templates"

blueprint: flask.Blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)	
login_manager: flogin.LoginManager = flogin.LoginManager()
courier: Courier = Courier()
session = Session.create_session()
	
def init(self, folder: str, app: flask.Flask):
	global blueprint
	global login
	blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)	
	login_manager.setup_app(app)

def setTemplateFolder(self, folder="templates"):
	global blueprint
	blueprint = flask.Blueprint('user_api', __name__, template_folder=folder)	

def setApp(app):
	global login
	login_manager.setup_app(app)

def getBlueprint() -> flask.Blueprint:
	return blueprint

@blueprint.route('/registration', methods=['GET', 'POST'])
def register():
	if flogin.current_user.is_authenticated:
		return flask.redirect('/')
	if flask.request.method == 'GET':
		courier.reloadBar(menu_activated=None, user=flogin.current_user.is_authenticated)
		menu = {}
		menu["menu"] = courier.get_Home()
		return flask.render_template('registration.html', title='Registration on ICA', menu=menu)

	elif flask.request.method == 'POST':

		return flask.redirect("/")


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if flogin.current_user.is_authenticated:
		return flask.redirect('/')
	if flask.request.method == 'GET':
		courier.reloadBar(menu_activated=None	, user=flogin.current_user.is_authenticated)
		menu = {}
		menu["menu"] = courier.get_Home()
		return flask.render_template('login.html', title='Sign In', menu=menu)
	elif flask.request.method == 'POST':
		data = flask.request.form
		user = session.query(User).filter( (User.name==data['login']) | ((User.email==data['login']))).first()
		print(data)
		if user is None or not user.check_password(data['password']):
			flask.flash(f"Invalid username or password: login: {data['login']}, password: {data['password']}")
			return flask.redirect(flask.url_for('login'))
			
		login_user(user, remember=data['remember_me'])
		# if not flogin.is_safe_url(next):	return flask.abort(400)
			
		return flask.redirect("/")
		

@blueprint.route('/logout')
def logout():
	flogin.logout_user()
	return flask.redirect('/')

@login_manager.user_loader
def load_user(id):
	return session.query(User).filter( User.id==int(id) ).first()
 

'''
@Service.blueprint.route('/login', methods=['GET', 'POST'])
def login():
	if flogin.current_user.is_authenticated:
		return flask.redirect('/')

	if flask.request.method == 'GET':
		courier.reloadBar(menu_activated="Images", user=flogin.current_user.is_authenticated)
		menu = {}
		menu["menu"] = courier.get_Home()
		return flask.render_template('login.html', title='Sign In', menu=menu)

	elif flask.request.method == 'POST':
		data = flask.request.form
		user = session.query(User).filter( (User.name==data['login']) | ((User.email==data['login']))).first()
		print(data)

		if user is None or not user.check_password(data['password']):
			flask.flash(f"Invalid username or password: login: {data['login']}, password: {data['password']}")
			return flask.redirect(flask.url_for('login'))
			
		login_user(user, remember=data['remember_me'])
		# if not flogin.is_safe_url(next):	return flask.abort(400)
			
		return flask.redirect("/")

@Service.blueprint.route('/logout')
def logout():
	flogin.logout_user()
	return flask.redirect('/')

@Service.login.user_loader
def load_user(id):
	return session.query(User).filter( User.id==int(id) ).first()
'''