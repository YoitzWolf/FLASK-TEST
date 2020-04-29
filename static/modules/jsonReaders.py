# -*- coding: utf-8 -*-
import json
import sys


def createHtmlByDict(self, data, item, inside=None):
	dict = data['item']

	html = f"<dict['tag'] {' '.join(['{}={}'.format(x, '%DOC%'+dict['tag_attributes'][x]+'%DOC%') for x in dict['tag_attributes']])} >\n".replace('%DOC%', '"')
	if inside is None and "inside" in dict:

		if "insize-type" not in dict or dict["inside-type"] == "text":
			html += dict['inside']

		elif dict["inside-type"] == "html":
			html += createHtmlByDict(data, dict['inside'])

	html = f"</dict['tag']>"

	return html

def readMenu(adress, activated="None", user=False):
	document = ''
	userfield = ''
	data = ''

	with open(adress, "r") as read_file:
		data = json.load(read_file)


	for item in data['menu']:
		if(item['tag_attributes']['id']==activated): item['tag_attributes']['class'] += " active"

		document += (f"<{item['tag']} {' '.join(['{}={}'.format(x, '%DOC%'+item['tag_attributes'][x]+'%DOC%') for x in item['tag_attributes']])} >\n").replace('%DOC%', '"')

		document += (f"<a {' '.join(['{}=%DOC%{}%DOC%'.format(x, item['link_attributes'][x]) for x in item['link_attributes']])}>").replace('%DOC%', '"')

		document += f"{item['text']}</a>"

		document += f"</{item['tag']}>\n"

	if user:
		userfield += (f"<{data['sign-menu']['autorized']['tag']} {' '.join(['{}={}'.format(x, '%DOC%'+data['sign-menu']['autorized']['tag_attributes'][x]+'%DOC%') for x in data['sign-menu']['autorized']['tag_attributes']])} >\n").replace('%DOC%', '"')

		userfield += (f"<a {' '.join(['{}=%DOC%{}%DOC%'.format(x, data['sign-menu']['autorized']['link_attributes'][x]) for x in data['sign-menu']['autorized']['link_attributes']])}>").replace('%DOC%', '"')

		userfield += f"{data['sign-menu']['autorized']['text']}</a>"

		userfield += f"</{data['sign-menu']['autorized']['tag']}>\n"
		
	else:
		userfield += (f"<{data['sign-menu']['unautorized']['tag']} {' '.join(['{}={}'.format(x, '%DOC%'+data['sign-menu']['unautorized']['tag_attributes'][x]+'%DOC%') for x in data['sign-menu']['unautorized']['tag_attributes']])} >\n").replace('%DOC%', '"')

		userfield += (f"<a {' '.join(['{}=%DOC%{}%DOC%'.format(x, data['sign-menu']['unautorized']['link_attributes'][x]) for x in data['sign-menu']['unautorized']['link_attributes']])}>").replace('%DOC%', '"')

		userfield += f"{data['sign-menu']['unautorized']['text']}</a>"

		userfield += f"</{data['sign-menu']['unautorized']['tag']}>\n"

	return document, userfield

def testJSONCompiler(adress):
	with open(adress, "r") as read_file:
		data = json.load(read_file)
		return createHtmlByDict(data, "")

if __name__ == '__main__':
	print(readMenu("../site-json/top-menu.json", activated="Home"))