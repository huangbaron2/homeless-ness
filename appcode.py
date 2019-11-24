import os.path
import csv
import json
import urllib.request
import sqlite3

def clearYear():
	with open ('year.txt', 'w') as f:
		f.write('2009')

clearYear()

def loadData(csvFile, howMany):
	if not os.path.isfile(csvFile):
		params = urllib.parse.urlencode({"$limit":howMany})
		uri = "https://data.cityofnewyork.us/api/views/5t4n-d72c/rows.json?%s" % params
		response = urllib.request.urlopen(uri)
		content_string = response.read().decode()
		content = json.loads(content_string)
		for i in content.get('data'):
			conn = sqlite3.connect(csvFile)
			cur = conn.cursor()
			cur.execute('CREATE TABLE IF NOT EXISTS insurance (value, place, years)')
			cur.execute('INSERT INTO insurance VALUES (?, ?, ?)', (i[-1], i[-3], i[-2]))
			#(Value, Year, Place)
			conn.commit()
	conn = sqlite3.connect(csvFile)
	cur = conn.cursor()
	re = cur.execute('SELECT * FROM insurance')
	#for row in re:
		#print(row)
	conn.close()
		
loadData('insurance.db', 1000)

def get_year():
	newlst = []
	conn = sqlite3.connect('insurance.db')
	cur = conn.cursor()
	re = cur.execute('SELECT * FROM insurance')
	for row in re:
		newlst.append(list(row))
	conn.close()
	return newlst

def makePie():
	#(Value, Year, Place)
	a = get_year()
	place = []
	value = []
	with open ('year.txt', 'r') as f:
		for line in f:
			yeartxt = json.loads(line)
	for i in a:
		if str(yeartxt) == str(i[1]):
			place.append(i[2])
			value.append(int(i[0]))
	value = value[0:15]
	place = place[0:15]
	title = 'Homelessness in ' + str(yeartxt)
	data = [{
		'values': value, 
		'labels': place, 
		'type': 'pie'}]
	layout = {
		'title': title,
		'name': 'New York City Homeslessness Population',
		'hoverinfo': 'label+percent+name',
		'height': 500,
		'width': 1000,
		'textAlign': 'center'
	}
	return {'data': data, 'div': 'yearGraph', 'layout': layout}

def makeTable():
	#(Value, Year, Place)
	outerDic = {}
	company = []
	companyPLAIN = []
	headerValues= [['<b>Years<b>'], ['<b>2009<b>'], ['<b>2010<b>'], ['<b>2011<b>'], ['<b>2012<b>']]
	cellsValues = []
	conn = sqlite3.connect('insurance.db')
	cur = conn.cursor()
	re = cur.execute('SELECT * FROM insurance')
	for row in re:
		if row[2] not in companyPLAIN:
			company.append("<b>" + row[2] + "<b>")
			companyPLAIN.append(row[2])
	conn.close()
	cellsValues.append(company)
	for years in range(2009, 2013):
		complaints = []
		conn = sqlite3.connect('insurance.db')
		cur = conn.cursor()
		year = str(years)
		re = cur.execute('SELECT * FROM insurance')
		newlst = []
		for rows in re:
			if rows[1] == year:
				newlst.append(rows[0])
		cellsValues.append(newlst)
	data = [{
		'type': 'table',
		'header': {
			'values': headerValues,
			'fill': {'color': '#e6f9ff'},
		},
		'cells':{
			'values': cellsValues,
			'fill': {'color': ['#e6ffe6', 'white']},
			'align': ["left", "center"]
			}
		}]
	layout = {
		'title': 'NYC Homeslessness Data for All Years',
		'height': 600,
		'width': 1000,
		'textAlign': 'center'
	}
	a = [data, layout]
	return a

def receive_year(x):
	with open ('year.txt', 'w') as f:
		f.write(x)