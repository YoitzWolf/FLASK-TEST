# -*- coding: utf-8 -*-
import flask
import flask_wtf as wtf
import flask_login as flogin
from flask_login import current_user, login_user
import os
from static.modules.config import Config, Courier
from static.modules.alchemy.users import User, userFabric
from werkzeug.utils import secure_filename

from static.modules.alchemy import session as Session

ROOT = True

app = flask.Flask(__name__)
app.config.from_object(Config)

login = flogin.LoginManager(app)
courier = Courier()

session = None

@app.route('/')
def main():
	courier.reloadBar(menu_activated="Home", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()

	page_header = "Welcome to International Colonisation Agency!"
	page_header_text = "Colonisation Center"
	h_image = "./static/img/cosmos-1.jpg"
	return flask.render_template("home.html", title="Colonisation Agency", page_header=page_header, page_header_text=page_header_text, h_image=h_image, menu=menu);


@app.route('/test-questionary', methods=['GET', 'POST'])
def quest():
	if flask.request.method == "GET":
		courier.reloadBar(menu_activated="Registration", user=flogin.current_user.is_authenticated)
		menu = courier.get_fullmenu()

		page_header = "Apllicant Blank Form №.a001"
		page_header_text = "Анкета претендента на участие в миссии ICA"
		return flask.render_template("blank.html", title="Astronaut Blank", page_header=page_header, page_header_text=page_header_text, menu=menu);

	elif flask.request.method == 'POST':
		print(flask.request.form.get("name"))
		print(flask.request.form.get("surname"))
		print(flask.request.files['photo'])
		return "<h1>Confirm</h1>"


@app.route('/results/<string:nickname>/<int:level>/<float:raiting>')
def result_viewer(nickname=None, level=0, raiting=0):
	courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()
	return flask.render_template("rate-view.html", title="Result Blank", user=nickname, level=level, rate=raiting, menu=menu);


@app.route('/choice/<string:planet>')
def added_variant(planet=None):
	courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()

	page_header = "Mission Blank №.1"
	page_header_text = "Банк идей будущих миссии ICA"
	data = '''
		<h2>Idea</h2>
		<h4 class="alert alert-primary">
			Хорошая планета
		</h4>
		<h4 class="alert alert-primary">
			Ресурсы есть, наверное...
		</h4>
		<h4 class="alert alert-primary">
			А еще там жизнь есть, возможно..
		</h4>

		'''
	return flask.render_template("planet-variant-1.html", planet=planet, data=data, title="Planet Blank", page_header=page_header, page_header_text=page_header_text, menu=menu);

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if flask.request.method == 'GET':
		courier.reloadBar(menu_activated="Images", user=flogin.current_user.is_authenticated)
		menu = courier.get_fullmenu()

		images = courier.get_uploaded_images("./static/uploads/.")

		page_header = "Load Image"
		page_header_text = "anonimous image loader"
		return flask.render_template("upload.html", title="Image Blank", page_header=page_header, page_header_text=page_header_text, menu=menu, images=images);
	elif flask.request.method == 'POST':
		file = flask.request.files['photo']
		if file.filename == '':
			flask.flash('No selected file')
			return flask.redirect(flask.request.url)
		else:
			filename = secure_filename(file.filename)
			file.save("static/uploads/" + filename)
			return flask.redirect(flask.url_for('upload'))
		return "<h1>Confirm</h1>"


@app.route('/images')
def image_viewer():
	courier.reloadBar(menu_activated="Images", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()
	all_upl_images = courier.get_uploaded_images("./static/uploads/.")

	caroucel = "1"#courier.get_caroucel("./static/uploads/.")

	page_header = "Load Image"
	page_header_text = "anonimous image loader"

	return flask.render_template("image-view.html", title="Images", page_header=page_header, page_header_text=page_header_text, menu=menu, images_upl=all_upl_images, caroucel=caroucel);


@app.route('/choice')
def add_variant():
	courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()

	page_header = "New Mission Blank Form №.1"
	page_header_text = "Анкета предложения новой миссии ICA"
	return flask.render_template("planet-blank-1.html", title="New Planet Blank", page_header=page_header, page_header_text=page_header_text, menu=menu);


@app.errorhandler(404)
def no_such_page(error):
	courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()

	return flask.render_template("main.html", title="Error 404", name='Interntional Colonisation Agency', menu=menu, error=f"<h1>No such page!</h1><h5>Error: {error}</h5>")


@app.route('/<string:planet>/test')
def mars_test(planet=None):
	courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
	menu = courier.get_fullmenu()
	menu["menu"] = courier.get_Home()
	
	return flask.render_template("mission-base.html", title="Mission", menu=menu, planet=planet);

@app.route('/<string:planet>/main')
def mission_main(planet=None):
	if planet is not None:
		planet = planet.lower()
		courier.reloadBar(menu_activated="None", user=flogin.current_user.is_authenticated)
		menu = courier.get_fullmenu()
		menu["menu"] = courier.get_Home()
		if planet: menu["menu"] += courier.get_BarLink_To(link=f"/{planet}/main", text=planet.title())
		
		return flask.render_template("mission-base.html", title="Mission", menu=menu, planet=planet);

	else: return no_such_page(404)

#--------------------------------LOGIN-------------------------------------

@login.user_loader
def load_user(id):
	return session.query(User).filter( User.id==int(id) ).first()

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
	flogin.logout_user()
	return flask.redirect('/')

def addRoot():
	user = User()
	user.name = "root"
	user.surname = ""
	user.set_password("root")
	user.email = "yoitz@yandex.ru"
	session = Session.create_session()
	session.add(user)
	session.commit()

def addCaptainAndThreeRandomUsers():

	session = Session.create_session()

	user = User()
	user.name = "Ridley"
	user.surname = "Scott"
	user.age = 21
	user.position = "captain"
	user.speciality = "research engineer"
	user.adress = "module_1"
	user.set_password("password")
	user.email = "scott_chief@mars.org"
	session.add(user)

	user = User()
	user.name = "Ein"
	user.surname = "Corgi"
	user.age = 24
	user.position = "data_dog"
	user.speciality = "dog"
	user.adress = "Edward`s_bed"
	user.set_password("rhhaw!")
	user.email = "best_e_mail_adress_you_never_forget@mars.org"
	session.add(user)

	user = User()
	user.name = "Edward"
	user.surname = "Wong Hau Pepelu Tivruski IV"
	user.age = 13
	user.position = "cool_hacker"
	user.speciality = "programming"
	user.adress = "module_1"
	user.set_password("iamagirl")
	user.email = "ediscool@mars.org"
	session.add(user)


	user = User()
	user.name = "Spike"
	user.surname = "Spiegel"
	user.age = 27
	user.position = "cowboy"
	user.speciality = "space_cowboy"
	user.adress = "module_1"
	user.set_password("swordfishII")
	user.email = "see_you_space_cowboy@mars.org"
	session.add(user)



	session.commit()


if __name__ == '__main__':
	result = Session.global_init("./static/db/db.sqlite") # init BaseName
	print("DB COONECTION :::: ", result)
	if result == "OK":
		try:
			addCaptainAndThreeRandomUsers()
		except Exception as e:
			print("Task \"Добавляем капитана\" cannot be completed => The same names in table users. Delete file or just check task.")

		session = Session.create_session()
		#app.run(host='localhost', port=8080)
		session.commit()
