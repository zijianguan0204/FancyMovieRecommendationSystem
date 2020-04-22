from flask import Flask, render_template, request, json, jsonify
import mysql.connector
from mysql.connector import Error
import json
app = Flask(__name__)

posts = [
	{
		'author': 'zhadanren',
		'title' : 'Blog post 1',
		'content': 'something...',
		'date_posted' : 'date here....'	
	},
	{
		'author': 'zhadanren',
		'title' : 'Blog post 1',
		'content': 'something...',
		'date_posted' : 'date here....'	
	}
]

try:
	connection = mysql.connector.connect(host='localhost',
	                                     database='movie_recommender',
	                                     user='root',
	                                     password='')
	if connection.is_connected():
	    db_Info = connection.get_server_info()
	    print("Connected to MySQL Server version ", db_Info)
	    cursor = connection.cursor()

except Error as e:
    print("Error while connecting to MySQL", e)


# @app.route('/')
# def hello_world():
#     return render_template('home.html', posts = posts)

@app.route('/movie')
def movie():
	
	
	movieId = request.args.get('movieId')
	print(movieId)
	movieId = 862

	title_sql = "SELECT DISTINCT original_title FROM movies_metadata WHERE id = %s"
	cursor.execute(title_sql, (movieId,)) #sql query..... 
	row = cursor.fetchone()
	title = row[0]

	genres_sql = "SELECT DISTINCT genres FROM movies_metadata WHERE id = %s"
	cursor.execute(genres_sql, (movieId,)) #sql query..... 
	row = cursor.fetchone()
	genres = row[0]
	print(genres)
	genres_json = json.dumps(genres)
	print(genres_json)
	# genres_string = json.loads(genres)
	# genres_json = json.dumps(genres_string)
	# name = genres_json["name"]

	release_date_sql = "SELECT DISTINCT release_date FROM movies_metadata WHERE id = %s"
	cursor.execute(release_date_sql, (movieId,)) #sql query..... 
	row = cursor.fetchone()
	release_date = row[0]

	# title_sql = "SELECT DISTINCT original_title FROM movies_metadata WHERE id = %s"
	# cursor.execute(sql, (movieId,)) #sql query..... 
	# row = cursor.fetchone()
	# title = row[0]
	

	data = {
    'title':title,
    'genre':"genres_type",
    'poster':'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',
    'director': 'Someone...',
    'actor':'Emma Watson',
    'avg_rating':4,
    'released':release_date,
    'description':'Harry Potter 4',
    'user_rating':-1}
	
	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response



if __name__=='__main__':
	app.run(debug=True)