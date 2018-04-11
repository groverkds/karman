from __future__ import print_function, absolute_import, division
import os
import sys
import numpy
import nltk
import datetime
import requests
import json
import xmltodict
import wikipedia
import urllib

oxford_app_id = '2c3e82dd'
oxford_app_key = '6c8daa6f8472d2d330208f444a9d2e88'
def DUCK_DUCK_GO_SEARCH(tokens):
	word = tokens[0]
	for token in tokens[1:len(tokens)]:
		word = word + '+' + token
	reply = 'Not a valid word'
	try:
		searchResults = requests.get('https://api.duckduckgo.com/?q='+word+'&format=json')
		reply = (searchResults.json())['RelatedTopics'][0]['Text']
		tkn=nltk.word_tokenize(reply)
		if tkn[-1]=='Category':
			reply = (searchResults.json())['Abstract']
	except:
		reply = 'Not a valid word'
	return reply
def WikiSearch(tokens):
	word = tokens[0]
	for token in tokens[1:len(tokens)]:
		word = word + ' ' + token
	reply = 'Not a valid word'
	try:
		reply = wikipedia.summary(word, sentences = 1)
	except:
		pass
	return reply
def FUN_DICT(tokens):
	word = tokens[0]
	for token in tokens[1:len(tokens)-1]:
		word = word + '+' + token
	reply = 'Not a valid word'
	try:
		url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower()
		r = requests.get(url, headers = {'app_id': oxford_app_id, 'app_key': oxford_app_key})
		#print("code {}\n".format(r.status_code))
		#print("text \n" + r.text)
		#print("json \n" + json.dumps(r.json()))
		r = r.json()
		reply = r['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
	except:
		pass
	if reply == 'Not a valid word':
		reply = WikiSearch(tokens)
	#if reply == 'Not a valid word':
	#	reply = DUCK_DUCK_GO_SEARCH(tokens)
	return reply

def FUN_NOW_TIME(tokens):
	t = datetime.datetime.now()	
	reply = 'Time is ' + str(t.hour) + ' hours and ' + str(t.minute) + ' minutes' 
	if tokens == None or 'TIME' in tokens:
		pass
	elif 'DAY' in tokens:
		reply = 'Today is ' + t.strftime("%A")
	elif 'MONTH' in tokens:
		reply = 'Current month is ' + t.strftime("%B")
	elif 'YEAR' in tokens:
		reply = 'Current year is ' + str(t.year)
	return reply
def FUN_TIME_DIFF(tokens):
	d1 = datetime.date.today()
	d2 = datetime.date(int(tokens[2]),int(tokens[1]),int(tokens[0]))
	diff = d2 - d1
	return(str(diff.days) + ' days to go for ' + str(d2))
def FUN_WEATHER(tokens):
	
	weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Vadodara&APPID=d2002bab2266867de9d23074615d6925')
	wjdata=weather.json()
	temperature = float(wjdata['main']['temp'])-273
	description = wjdata['weather'][0]['description']
			
	reply = 'Temperature is ' + str(str(round(temperature, 2))) + ' celsius. Presently weather is ' + description		
	if tokens[0] == None:
		pass
	else:
		city = tokens[0]
		for token in tokens[1:len(tokens)]:
			city = city + '+' + token
		weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=d2002bab2266867de9d23074615d6925')
		wjdata=weather.json()
		temperature = float(wjdata['main']['temp'])-273
		description = wjdata['weather'][0]['description']
		reply = 'Temperature is ' + str(str(round(temperature, 2))) + ' celsius. Presently weather is ' + description + '.'
	return reply

def FUN_STOCK(tokens):
	stock = tokens[0]
	stock_data = requests.get('http://dev.markitondemand.com/MODApis/Api/v2/Quote?Symbol='+stock)
	o = xmltodict.parse(stock_data.content)
	a = json.dumps(o)
	a = json.loads(a)
	reply = 'Stock quote is not valid'
	try:
		name = a["StockQuote"]["Name"]
		symbol = a["StockQuote"]["Symbol"]
		price = a["StockQuote"]["LastPrice"]
		reply = 'Stock of '+name+' ('+symbol+') is priced at $'+price
	except:
		pass
	return reply

def Calculator(tokens):
	operation = tokens[0]
	if operation == 'add':
		reply = str(float(tokens[1]) + float(tokens[2]))
	elif operation == 'subtract':
		reply = str(float(tokens[1]) - float(tokens[2]))
	elif operation == 'multiply':
		reply = str(float(tokens[1]) * float(tokens[2]))	
	elif operation == 'divide':
		if tokens[2] != 0.0:
			try:
				reply = str(float(tokens[1]) / float(tokens[2]))
			except:
				reply = 'Cannot divide by 0'
	elif operation == 'CALCULATOR':
		tokens.remove('CALCULATOR')
		expr = tokens[0]
		for token in tokens[1:len(tokens)]:
			expr = expr + token
		reply = 'Ans: ' + str(eval(expr))
	return reply

def GetNews(tokens):
	reply = "No news"
	if('CATEGORY' in tokens):
		tokens.remove('CATEGORY')
		cat = tokens[0]
		for token in tokens[1:len(tokens)]:
			cat = cat + ' ' +token
		#cat = urllib.parse.quote(cat, safe='')
		url = 'https://newsapi.org/v2/top-headlines?q=' + cat + '&apiKey=c9b7deaa342c4216a28a63561a5f18e3'
		response = (json.loads((requests.get(url).content).decode('UTF-8')))
		articles = response['articles']
		#totalResults = int(response['totalResults'])
		#print(response)
		reply = ""
		try:			
			for i in range(5):
				reply = reply + '<a href='+articles[i]['url']+'>'+articles[i]['title'] + "<a/><br><br>"			
		except:
			pass
	else:
		url = 'https://newsapi.org/v2/top-headlines?country=' + tokens[0] + '&apiKey=c9b7deaa342c4216a28a63561a5f18e3'
		response = (json.loads((requests.get(url).content).decode('UTF-8')))
		articles = response['articles']
		#totalResults = int(response['totalResults'])
		#print(response)
		reply = ""
		try:			
			for i in range(5):
				reply = reply + '<a href='+articles[i]['url']+'>'+articles[i]['title'] + "<a/><br><br>"			
		except:
			pass
	return reply
def FUN_TIME_GREET(tokens):
	reply = 'Hey'
	try:
		t = datetime.datetime.now()
		if(4 <= t.hour < 12):
			reply = 'Good Morning!'
		elif(12 <= t.hour < 4):
			reply = 'Good Afternoon!'
		elif(4 <= t.hour < 12):
			reply = 'Good Evening!'
		elif(4 <= t.hour < 4):
			reply = 'Good Night! Its probably your time to sleep!'
	except:
		pass
	return reply

def Reply(message):
	reply = message
	tokens=nltk.word_tokenize(message)
	try:
		if 'FUN_NOW_TIME' in tokens:
			tokens.remove('FUN_NOW_TIME')
			reply = FUN_NOW_TIME(tokens)
		elif 'FUN_WEATHER' in tokens:
			tokens.remove('FUN_WEATHER')
			reply = FUN_WEATHER(tokens)
		elif 'FUN_TIME_DIFF' in tokens:
			tokens.remove('FUN_TIME_DIFF')
			reply = FUN_TIME_DIFF(tokens)
		elif 'FUN_STOCK' in tokens:
			tokens.remove('FUN_STOCK')
			reply = FUN_STOCK(tokens)
		elif 'FUN_DICT' in tokens:
			tokens.remove('FUN_DICT')
			reply = FUN_DICT(tokens)
		elif 'FUN_SEARCH' in tokens:
			tokens.remove('FUN_SEARCH')
			reply = FUN_DICT(tokens)
		elif 'FUN_PERSON_SEARCH' in tokens:
			tokens.remove('FUN_PERSON_SEARCH')
			reply = WikiSearch(tokens)
		elif 'FUN_CALC' in tokens:
			tokens.remove('FUN_CALC')
			reply = Calculator(tokens)
		elif 'FUN_NEWS' in tokens:
			tokens.remove('FUN_NEWS')
			reply = GetNews(tokens)
		elif 'FUN_TIME_GREET' in tokens:
			tokens.remove('FUN_TIME_GREET')
			reply = FUN_TIME_GREET(tokens)
		'''elif 'FUN_HOROSCOPE' in tokens:
			tokens.remove('FUN_HOROSCOPE')
			reply = FUN_HOROSCOPE(tokens)'''
	except:
		reply = 'I ran into some error'
	return {'reply': reply}