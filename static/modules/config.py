import os
from static.modules.jsonReaders import readMenu


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'one-hundred-percents-random-key-you-never-hack'
    UPLOAD_FOLDER = '/uploads'
    FLASK_ENV = "development"
    FLASK_DEBUG = 1
    DEBUG = True


class Courier(object):
	""" <<Courier>> site-data manager """

	def setConfigByKey(self, key, value):
		self.__dict__[key] = value

	def get_uploaded_images(self, path):
		data = os.listdir(path=path)
		doc = ""
		for i in data:
			doc += f"<img alt='{i}' title='{i}' class='imager-200-height shadow-hover-dark' style='margin:0.5em;' src='{path[:-1]+i}' >"
		return doc

	def get_menu(self):
		return self.data['menu']

	def get_signMenu(self):
		return self.data['userfield']

	def get_fullmenu(self):
		return {
					"menu": self.get_menu(),
					"userfield": self.get_signMenu()
				}

	def reloadBar(self, menu_activated="None", user=False):
		self.data['menu'], self.data['userfield'] = readMenu("./static/site-json/top-menu.json", activated=menu_activated, user=user)

	def get_Home(self, planet, user=False):
		return """<li id="Home" class="nav-item"><a class="nav-link" href="/">Home</a></li>"""

	def __init__(self):
		self.data = {}
		self.reloadBar()


if __name__ == '__main__':
	auto = Courier()
	auto.setConfig("menu", "some shit")
	print(auto.menu)
		