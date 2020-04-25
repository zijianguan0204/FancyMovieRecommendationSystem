from flask import Flask, render_template, request, json, jsonify
import mysql.connector
import ast
from mysql.connector import Error
import json
from movie_recommender import movie_recommender
import datetime
from datetime import timedelta

app = Flask(__name__)

# Connect to Database
try:
	connection = mysql.connector.connect(host='localhost',
	                                     database='movie_Recommender',
	                                     user='root',
										 password='') #zijian
										#  auth_plugin='mysql_native_password', # V
	                                    #  password='leoJ0205') # V
	if connection.is_connected():
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor()

except Error as e:
    print("Error while connecting to MySQL", e)

# Get movie detail according to movie ID and user ID
@app.route('/movie')
def movie():
	
	print("hello")
	movieId = request.args.get('movieId')
	userId = int(request.args.get('userId'))
	# print(movieId)
	# print(userId)
	# test
	# movieId = 862
	# userId = 2103

	# initialization
	id = ''
	title = ''
	poster = ''
	release_date = ''
	description = ''
	genres_str = ''
	ave_rating = ''
	actors_str = ''
	director_str = ''

	# get movie meta info
	sql = "SELECT id, title, poster_path, release_date, overview, vote_average " \
		  "FROM movies_metadata " \
		  "WHERE id = %s"
	cursor.execute(sql, (movieId,)) 
	row = cursor.fetchone()
	if row != None:
		id = row[0]
		title = row[1]
		poster = row[2]
		release_date = row[3]
		description = row[4]
		ave_rating = str(row[5])

	# get movie genres
	sql = "SELECT genre " \
		  "FROM movie_genre " \
		  "WHERE id = %s"
	cursor.execute(sql, (movieId,))
	genres_dr= cursor.fetchall()
	if genres_dr != None:
		for genre in genres_dr:
			genres_str += genre[0] + ','
		genres_str = genres_str[:-1]

	# get average rating
	# sql = "SELECT AVG(rating) AS ave_rating " \
	# 	  "FROM ratings " \
	# 	  "WHERE movieid = %s"
	# cursor.execute(sql, (movieId,))
	# ave_rating_dr = cursor.fetchone()
	# ave_rating = ave_rating_dr[0]

	# get user rating
	sql = "SELECT rating " \
		  "FROM ratings " \
		  "WHERE movieid = %s " \
		  "AND userid = %s"
	cursor.execute(sql, (movieId, userId,))
	user_rating_dr = cursor.fetchone()
	user_rating = None if (user_rating_dr == None) else user_rating_dr[0][:-1] 

	# get actors (cast)
	sql = "SELECT name " \
		  "FROM movie_Recommender.cast_infor " \
		  "INNER JOIN movie_cast " \
		  "ON cast_infor.id = movie_cast.cast_id " \
		  "WHERE movie_id = %s"
	cursor.execute(sql, (movieId,))
	actors_dr = cursor.fetchall()
	if actors_dr != None:
		for actor in actors_dr:
			actors_str += actor[0][:-1] + ','
			# actors_str += actor[0] + ','
		actors_str = actors_str[:-1]

	# get director (crew)
	sql = "SELECT name " \
		  "FROM crew_info " \
		  "INNER JOIN movie_crew " \
		  "ON crew_info.id = movie_crew.crew_id " \
		  "WHERE movie_id = %s " \
		  "AND upper(job) = upper('director')"
	cursor.execute(sql, (movieId,))
	director_dr = cursor.fetchall()
	if director_dr != None:
		for director in director_dr:
			director_str += director[0][:-1] + ','
			# director_str += director[0] + ','
		director_str = director_str[:-1]

	data = {
		'id':id,
		'title':title,
		'genre':genres_str,
		'poster':poster,
		'director': director_str,
		'actor':actors_str,
		'avg_rating':ave_rating,
		'released':release_date,
		'description':description,
		'user_rating':user_rating
		}

	cursor.close()

	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# Search for movie(s)
@app.route('/movieSearch')
def movie_search():
	# test
	# search_input = 'Harry Potter'
	search_input = request.args.get('search')

	sql = "SELECT id, title, poster_path " \
		  "FROM movies_metadata " \
		  "WHERE upper(title) like concat(upper(%s), '%')"
	cursor.execute(sql, (search_input.strip(),)) 
	rows = cursor.fetchall()

	cursor.close()	

	x = {} # each row
	result = []
	for row in rows:
		x['id'] = row[0]
		x['title'] = row[1]
		x['poster'] = row[2]
		result.append(x)
	# response = jsonify(dict(rows))
	response = jsonify(result)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# # Get user's rating history
@app.route('/moviesRating')
def user_rating_history():
	# test
	# userid = 2103
	userid = int(request.args.get('userId'))

	sql = "SELECT id, title, poster_path, rating " \
		  "FROM movie_Recommender.ratings " \
		  "INNER JOIN movies_metadata " \
		  "ON ratings.movieid = movies_metadata.id " \
		  "WHERE userid = %s"
	cursor.execute(sql, (userid,)) 
	rows = cursor.fetchall()

	cursor.close()	

	x = {} # each row
	result = []
	for row in rows:
		x['id'] = row[0]
		x['title'] = row[1]
		x['poster'] = row[2]
		x['rating'] = row[3][:-1]
		result.append(x)
	# response = jsonify(dict(rows))
	response = jsonify(result)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

# Add/update user's new rating
@app.route('/moviesRating', methods = ['POST'])
def user_rating_upd():
	if request.headers['CONTENT_TYPE'] == 'application/json':
		movieId = request.json['movieId']
		userId = int(request.json['userId'])
		rating = request.json['rating']

		sql = "INSERT INTO ratings (movieid, userid, rating) " \
			f"VALUES ({movieId}, {userId}, {rating}) " \
			f"ON DUPLICATE KEY UPDATE rating = {rating}"
		try:
			cursor.execute(sql)
			connection.commit()
		except Error as e:
			print("Error while executing SQL", e)

		response = jsonify("")
		response.headers.add('Access-Control-Allow-Origin', '*')
		return response

# Get a list of recommended movies
@app.route('/movieSuggestion')
def movie_suggestion():
	# test
	# userid = 2103
	try:
		connection = mysql.connector.connect(host='localhost',
	                                     database='movie_Recommender',
	                                     user='root',
										 password='') #zijian
										#  auth_plugin='mysql_native_password', # V
	                                    #  password='leoJ0205') # V
		if connection.is_connected():
		    db_Info = connection.get_server_info()
		    print("Connected to MySQL Server version ", db_Info)
		    cursor = connection.cursor()

	except Error as e:
	    print("Error while connecting to MySQL", e)

	userid = request.args.get('userId')
	# userid = 1
	print(userid)
	var_list = [0.4, 0.2, 0.3, 0.05, 0.05]

# get all movie Id that the user rated >=4 into list
	sql = "SELECT movieId FROM movie_Recommender.ratings WHERE userid = %s AND rating >= 4"
	cursor.execute(sql,(userid,)) 
	rows = cursor.fetchall()
	movieid_list = []
	for tup in rows:
		movieid_list.append(tup[0])

# get all movie rated within 14 days into list
	recent_list = []
	for movieid in movieid_list:
		sql = "SELECT timestamp FROM movie_Recommender.ratings WHERE userid = %s AND movieid = %s"
		cursor.execute(sql,(userid, movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			cur_ts = tup[0].replace('\r', '') + '000'
			recent_list.append(cur_ts)

	recent_list.sort(reverse = True)
	if recent_list != []:
		most_recent_ts = recent_list[0]
		most_recent_date = datetime.datetime.fromtimestamp(float(cur_ts) / 1e3)
		date_before_14days = most_recent_date - timedelta(days=14)
		ts_before_14days = int(datetime.datetime.timestamp(date_before_14days)*1000)

	ts_list = []
	for ts in recent_list:
		if int(ts) >= ts_before_14days:
			ts_list.append(ts)

	final_movie_list = []
	for ts in ts_list:
		ts = str(int(int(ts)/1000))
		ts = ts + "\r"
		sql = "SELECT movieid FROM movie_Recommender.ratings WHERE userid = %s AND timestamp = %s"
		cursor.execute(sql,(userid, ts,))
		rows = cursor.fetchall()
		for tup in rows:
			final_movie_list.append(tup[0])

# add movie in the same collection into the recommend/unrecommend list
	recommend_list = []
	unrecommend_list = []
	collection_list = []
	for movieid in movieid_list:
		sql = "SELECT collection FROM movie_Recommender.movies_metadata WHERE id = %s"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if tup[0] > 0:
				collection_list.append(tup[0])
	
	for collection_id in collection_list:
		sql = "SELECT id FROM movie_Recommender.movies_metadata WHERE collection = %s"
		cursor.execute(sql,(collection_id,))
		rows = cursor.fetchall()
		count = 0
		for tup in rows:
			if count == 0:
				recommend_list.append(tup[0])
				count+=1
			else:
				unrecommend_list.append(tup[0])

#
			


# create a total dictionary
	total_dict = {}
# get all genres into dictionary
	genre_dict = {}
	for movieid in movieid_list:
		sql = "SELECT genre FROM movie_Recommender.movie_genre WHERE id = %s"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if tup[0] in genre_dict:
				genre_dict[tup[0]] += 1
			else:
				genre_dict[tup[0]] = 1
	total_dict.update(genre_dict)

# get all cast into dictionary
	cast_dict = {}
	for movieid in movieid_list:
		sql = "SELECT name FROM movie_Recommender.movie_cast INNER JOIN movie_Recommender.cast_infor WHERE cast_id = id AND movie_id = %s"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if tup[0] in cast_dict:
				cast_dict[tup[0]] += 1
			else:
				cast_dict[tup[0]] = 1
	total_dict.update(cast_dict)




# get all director into dictionary
	director_dict = {}
	for movieid in movieid_list:
		sql = "SELECT name FROM movie_Recommender.movie_crew INNER JOIN movie_Recommender.crew_info WHERE crew_id = id AND movie_id = %s AND job = 'Director\r'"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if tup[0] in director_dict:
				director_dict[tup[0]] += 1
			else:
				director_dict[tup[0]] = 1
	total_dict.update(director_dict)

# get all release_date into dictionary
	releaseDate_dict = {}
	for movieid in movieid_list:
		sql = "SELECT release_date FROM movies_metadata WHERE release_date >= '2000' AND id = %s"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if '>=2000' in releaseDate_dict:
				releaseDate_dict['>=2000'] += 1
			else:
				releaseDate_dict['>=2000'] = 1

		sql = "SELECT release_date FROM movies_metadata WHERE release_date < '2000' AND id = %s"
		cursor.execute(sql,(movieid,))
		rows = cursor.fetchall()
		for tup in rows:
			if '<2000' in releaseDate_dict:
				releaseDate_dict['<2000'] += 1
			else:
				releaseDate_dict['<2000'] = 1
	total_dict.update(releaseDate_dict)

#get top 15 tags
	top_tags = []
	for k in sorted(total_dict, key=total_dict.get, reverse=True):
		top_tags.append(k)

	if len(top_tags) > 15:
		top_tags = top_tags[0:14]



	return movie_recommender(userid)
    	
if __name__=='__main__':
	app.run(debug=True) # zijian
	# app.run(port=5001)