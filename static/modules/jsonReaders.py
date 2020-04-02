# -*- coding: utf-8 -*-
import json
import sys

def readMenu(adress, activated="NO DATA ACT"):
	document = ''
	with open(adress, "r") as read_file:
		data = json.load(read_file)


	for item in data['menu']:
		if(item['tag_attributes']['id']==activated): item['tag_attributes']['class'] += " active"

		document += (f"<{item['tag']} {' '.join(['{}={}'.format(x, '%DOC%'+item['tag_attributes'][x]+'%DOC%') for x in item['tag_attributes']])} >\n").replace('%DOC%', '"')

		document += (f"<a {' '.join(['{}=%DOC%{}%DOC%'.format(x, item['link_attributes'][x]) for x in item['link_attributes']])}>").replace('%DOC%', '"')

		document += f"{item['text']}</a>"

		document += f"</{item['tag']}>\n"

	return document


if __name__ == '__main__':
	print(readMenu("../site-json/top-menu.json", activated="Home"))