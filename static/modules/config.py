import os
from static.modules.jsonReaders import readMenu
import sqlalchemy as alchemy


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

	def load_news(self, session, unit, data=alchemy.sql.text("id > 0")):
		return session.query(unit).filter(data)

	def load_news_join(self, session, unit, data):
		return session.query(unit).all()

	def get_TablesFromList(self, data, json_context="marked-table", json_file="./static/site-json/tables.json", dict=None):
		table = ""
		for news in data:
			table += "<table class='light-table'>"

			table += "<tr class='table-head'>"
			if dict is None: dict = news.__dict__
			for item in dict:
					table += f"<td>{item}</td>"
			table += "</tr>"

			table += "<tr>"
			for item in dict:
					table += f"<td>{news.__dict__[item]}</td>"
			table += "</tr></table>"
		table += ""

		return table

	def get_TableBlocksFromList(self, data, json_context="marked-table", json_file="./static/site-json/tables.json", dict_to_table=None, header_field=""):
		table = ""
		for news in data:
			table += "<div class='center-block'>"
			head = news.__dict__[header_field] if header_field is not None and header_field in news.__dict__ else ""
			table += f"<h3>Action {head}</h3>"
			table += "<table class='light-table'>"

			table += "<tr class='table-head'>"
			if dict_to_table is None: dict_to_table = news.__dict__
			for item in dict_to_table:
					table += f"<td>{item}</td>"
			table += "</tr>"

			table += "<tr>"
			for item in dict_to_table:
					table += f"<td>{news.__dict__[item]}</td>"
			table += "</tr></table></div>"
		table += ""

		return table

	def get_Home(self):
		return """<li id="Home" class="nav-item"><a class="nav-link" href="/">Home</a></li>""" # usual Home

	def get_BarLink_To(self, link, text=None):
		if text is None: text = link
		return f"""<li id="Home" class="nav-item"><a class="nav-link" href="{link}">{text}</a></li>""" # usual Home		

	def __init__(self):
		self.data = {}
		self.reloadBar()


if __name__ == '__main__':
	auto = Courier()
	auto.setConfig("menu", "some shit")
	print(auto.menu)