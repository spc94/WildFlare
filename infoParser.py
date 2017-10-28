# -*- coding: utf-8 -*-
from facepy import GraphAPI
import json
import urllib2
import pymysql
import unidecode

token = "EAAB0TUhQia4BAOuukzuGIzjkYDlP01wpkMNXaYw76ZA7hL9EVLXZASW6t6vQ8KsmIPdeW3SZCByhCN4DAIKlpfW1eI07NLIeR11V4PLpZA8S8Vxph6ZAbJNdGytjRLtVxv8dRDcV3c6JoMIpMYb80XjKTFZAoZBFjd39sZB1IAJkXAZDZD"
graph = GraphAPI(token)
posts = graph.get('331909586894424')

APP_ID 	   = "127875274541486"
APP_SECRET = "dacd17a8d85398837d32d1dfd53c343c"

def connect_db():
	connection = pymysql.connect(user="root", password="",
											host = "127.0.0.1",
											database = "wildfire")
	return connection
	
def create_user_url(ID):
	user_url = "https://www.facebook.com/" + ID

	return user_url


def create_post_url(ID):
	post_url = "https://www.facebook.com/" + ID

	return post_url

def create_group_url(graph_url, APP_ID, APP_SECRET):
	post_args = "/feed/?key=value&access_token=" + APP_ID + "|" + APP_SECRET
	post_url = graph_url + post_args

	return post_url

def create_post_info_url(graph_url, APP_ID, APP_SECRET):
	post_args = "/?fields=from&key=value&access_token=" + APP_ID + "|" + APP_SECRET
	post_url = graph_url + post_args
	print "-DEBUG URL-----> " + post_url

	return post_url

def render_to_json(graph_url):
	try:
		web_response = urllib2.urlopen(graph_url)
		readable_page = web_response.read()
		json_data =json.loads(readable_page)
	except Exception, e:
		print str(e)
	return json_data

def main():
	#authentication keys
	APP_ID 	   = "127875274541486"
	APP_SECRET = "dacd17a8d85398837d32d1dfd53c343c"

	#different groups to iterate through
	list_groups = ["331909586894424", "150959922176926", "IDBraganca", "200806923402805", "1976532375951362", "627787477268700"]
	list_group_names = ["Madeira", "Aveiro", "Bragança", "Viseu", "Oliveira do Hospital", "Coimbra"]
	list_group_radio = ["https://www.jm-madeira.pt/radio","https://www.jornaldocentro.pt/emissao-online/", "http://www.brigantia.pt/radio", "https://www.jornaldocentro.pt/emissao-online/", "http://www.abss.pt/streaming/boanova/digitalrm_boanova_alt.html", "https://www.jornaldocentro.pt/emissao-online/"]
	graph_url = "https://graph.facebook.com/"

	#
	list_trigger_words = ["fogo", "chamas", "fumo", "bombeiros", "if", "incendio florestal"]
	list_trigger_points = [4,3,7,4,10,10]



	# creates a db connection
	connection = connect_db()
	cursor = connection.cursor()

	insert_info = ("INSERT INTO wildfire "
		"(situation, district, poster, publication, media, date, publication_url, user_url)"
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

	for j, group in enumerate(list_groups):
		# create a graph api url with current group
		current_page = graph_url + group

		# opens group as a page and then renders it to a json object
		group_url = create_group_url(current_page, APP_ID, APP_SECRET)


		json_groupdata = render_to_json(group_url)
		json_fbposts = json_groupdata['data']

		print "#### Group: " + group + " ####"
		for post in json_fbposts:
			score = 0
			location = ""
			print "----------------------"
			print "Post ID = " + post["id"]
			print "Message without accents: "
			try:
				print unidecode.unidecode(post["message"]).lower()
			except Exception, e:
				print "Unidecode Exception: " + str(e)
			# Scores the Message
			for i, word in enumerate(list_trigger_words):
				try:
					if word in unidecode.unidecode(post["message"]).lower():
						score = score + list_trigger_points[i]
				except Exception, e:
					print "Unicode Exception: " + str(e)

			print "Score = " + str(score)  
			location = list_group_names[j]
			print "Location = " + location
			

			graph_post_url = graph_url + post["id"]
			try:
				post_info_url  = create_post_info_url(graph_post_url, APP_ID, APP_SECRET)
			except Exception, e:
				print "Exception Create URL: " + unidecode.unidecode(e)
			print "url = " + post_info_url
			try:
				json_post_info_data = render_to_json(post_info_url)
			except Exception, e:
				poster = "John Doe"
				poster_id = 0000000000
				user_url = create_user_url(poster_id)
				post_url = create_post_url(post["id"])
				page_data = (score, location, poster, unidecode.unidecode(post["message"]), list_group_radio[j], post["updated_time"], post_url, user_url)
				cursor.execute(insert_info, page_data)
				connection.commit()
				print "Exception JSON: " + unidecode.unidecode(e) 
			try:
				json_post_info = json_post_info_data['from']
			except Exception, e:
				print "Exception JSON: " + unidecode.unidecode(e) 

			print "POSTER NAME: " 
			poster = unidecode.unidecode(json_post_info["name"])
			print poster

			print "USER ID: "
			poster_id = str(json_post_info["id"])
			print poster_id

			print "Profile URL: "
			user_url = create_user_url(poster_id)
			print user_url

			print "Post URL"
			post_url = create_post_url(post["id"])
			print post_url

				# Escreve para a DB
					# Poster ...
					# Publication é suposto ser apenas uma string construida com base no id do post
					# Contact é calculado com base nas informações do profile do poster
					# Media deve ser introduzido manualmente consoante o distrito
			try:
				page_data = (score, location, poster, unidecode.unidecode(post["message"]), list_group_radio[j], post["updated_time"], post_url, user_url)
				cursor.execute(insert_info, page_data)
				connection.commit()
			except Exception, e:
				try:
					page_data = (score, location, poster, unidecode.unidecode(post["message"]), list_group_radio[j], post["created_time"], post_url, user_url)
					cursor.execute(insert_info, page_data)
					connection.commit()
				except Exception,e:
					print "MySQL Exception: " + str(e)
				print "MySQL Exception: " + str(e)

		
	connection.close()

if __name__ == "__main__":
    main()   




