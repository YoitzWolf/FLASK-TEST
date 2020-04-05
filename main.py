# -*- coding: utf-8 -*-
import flask
import os
from static.modules.config import Config, Courier
from werkzeug.utils import secure_filename


app = flask.Flask(__name__)
app.config.from_object(Config)

courier = Courier()

@app.route('/')
def main():
	courier.reloadBar(menu_activated="Home", user=False)
	menu = courier.get_fullmenu()

	page_header = "Welcome to International Colonisation Agency!"
	page_header_text = "Colonisation Center"
	h_image = "./static/img/cosmos-1.jpg"
	return flask.render_template("home.html", title="Colonisation Agency", page_header=page_header, page_header_text=page_header_text, h_image=h_image, menu=menu);


@app.route('/test-questionary', methods=['GET', 'POST'])
def quest():
	if flask.request.method == "GET":
		courier.reloadBar(menu_activated="Registration", user=False)
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
	courier.reloadBar(menu_activated="None", user=False)
	menu = courier.get_fullmenu()
	return flask.render_template("rate-view.html", title="Result Blank", user=nickname, level=level, rate=raiting, menu=menu);


@app.route('/choice/<string:planet>')
def added_variant(planet=None):
	courier.reloadBar(menu_activated="None", user=False)
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
		courier.reloadBar(menu_activated="None", user=False)
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


@app.route('/choice')
def add_variant():
	courier.reloadBar(menu_activated="None", user=False)
	menu = courier.get_fullmenu()

	page_header = "New Mission Blank Form №.1"
	page_header_text = "Анкета предложения новой миссии ICA"
	return flask.render_template("planet-blank-1.html", title="New Planet Blank", page_header=page_header, page_header_text=page_header_text, menu=menu);

@app.errorhandler(404)
def no_such_page(error):
	courier.reloadBar(menu_activated="None", user=False)
	menu = courier.get_fullmenu()

	return flask.render_template("main.html", title="Error 404", name='Interntional Colonisation Agency', menu=menu, error=f"<h1>No such page!</h1><h5>Error: {error}</h5>")

'''
@app.route('/')
def main():
	return (
		f"{HEAD}"
		"<body>"

			"<div>"
				"<h1><a href=\"/\">MARS COLONISATION MISSION</a></h1>"
			"</div>"

			"<div style=\"color: lightcoral; font-size: 10pt;\">"
				"<a href=\"/index\">Немного информации о яблоках</a><br>"
				"<a href=\"/promotion_image\">Немного информации о рекламе</a><br>"
				"<a href=\"/image_mars\">Немного информации о Марсе</a><br>"
			"</div>"

		"</body>"
		)


@app.route('/index')
def index():
	return (
		f"{HEAD}"
		"<body>"

			"<div>"
				"<a href=\"/\"> BACK TO MAIN PAGE</a>"
			"</div>"

			"<div style=\"color: lightcoral; font-size: 10pt;\">"
				"И на Марсе будут яблони цвести!<br>"
			"</div>"

		"</body>"
		)


@app.route('/promotion')
def promotion():
	return (
		f"{HEAD}"
		"<body>"

			"<div>"
				"<a href=\"/\"> BACK TO MAIN PAGE</a>"
			"</div>"

			"<div style=\"color: lightcoral; font-size: 10pt;\">"
				"Человечество вырастает из детства.<br>"
				"Человечеству мала одна планета.<br>"
				"Мы сделаем обитаемыми безжизненные пока планеты.<br>"
				"И начнем с Марса!<br>"
				"Присоединяйся!<br>"
			"</div>"

		"</body>"
		)


@app.route('/image_mars')
def image_mars():
	return (
		f"{HEAD}"
		"<body>"

			"<div>"
				"<a href=\"/\"> BACK TO MAIN PAGE</a>"
			"</div>"

			"<div style=\"color: lightcoral; font-size: 10pt;\">"
				"<h1>Жди нас, Марс!</h1>"
				f"<img src={MARS} alt=\"mars\" style=\"width: 320px; margin: 20px;\">"
				"<br>"
				"Вот она - красная планета!<br>"
			"</div>"

		"</body>"
		)


@app.route('/promotion_image')
def promotion_image():
	return (
		f"{HEAD}"
		"<body>"
			"<div class=\"container\">"
				"<div>"
					"<a href=\"/\"> BACK TO MAIN PAGE</a>"
				"</div>"

				"<div style=\"color: lightcoral; font-size: 10pt;\">"
					"<h1>Жди нас, Марс!</h1>"
					f"<img src={MARS} alt=\"mars\" style=\"width: 320px; margin: 20px;\">"
					"<br>"

					"<div class=\" alert-danger\" style=\"padding: 5px;\">Человечество вырастает из детства.</div>"
					"<div class=\" alert-danger\" style=\"padding: 5px;\">Человечеству мала одна планета.</div>"
					"<div class=\" alert-danger\" style=\"padding: 5px;\">Мы сделаем обитаемыми безжизненные пока планеты.</div>"
					"<div class=\" alert-danger\" style=\"padding: 5px;\">И начнем с Марса!</div>"
					"<div class=\" alert-danger\" style=\"padding: 5px;\">Присоединяйся!</div>"

				"</div>"
			"</div>"
		"</body>"
		)
'''
if __name__ == '__main__':
	app.run(host='localhost', port=8080)