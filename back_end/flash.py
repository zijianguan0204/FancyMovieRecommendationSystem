from flask import Flask, render_template, request, json, jsonify

import mysql.connector
import ast

from flask_cors import cross_origin
from mysql.connector import Error
import json
from movie_recommender import movie_recommender
import datetime
from datetime import timedelta

app = Flask(__name__)

password = ''

# Connect to Database
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='movie_Recommender',
                                         user='root',
                                         password=password)  # zijian
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
@cross_origin()
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
        ave_rating = "%.2f" % row[5]

    # get movie genres
    sql = "SELECT genre " \
          "FROM movie_genre " \
          "WHERE id = %s"
    cursor.execute(sql, (movieId,))
    genres_dr = cursor.fetchall()
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
    user_rating = None if (user_rating_dr == None) else user_rating_dr[0]

    # get actors (cast)
    sql = "SELECT cast_infor.name " \
          "FROM movie_Recommender.cast_infor " \
          "INNER JOIN movie_cast " \
          "ON cast_infor.id = movie_cast.cast_id " \
          "WHERE movie_id = %s"
    cursor.execute(sql, (int(movieId),))
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
          "AND job = 'director\r'"
    cursor.execute(sql, (int(movieId),))
    director_dr = cursor.fetchall()
    if director_dr != None:
        for director in director_dr:
            director_str += director[0][:-1] + ','
        # director_str += director[0] + ','
        director_str = director_str[:-1]

    data = {
        'id': id,
        'title': title,
        'genre': genres_str,
        'poster': poster,
        'director': director_str,
        'actor': actors_str,
        'avg_rating': ave_rating,
        'released': release_date,
        'description': description,
        'user_rating': user_rating
    }

    # cursor.close()

    response = jsonify(data)
    return response


# Search for movie(s)
@app.route('/movieSearch')
@cross_origin()
def movie_search():
    # test
    # search_input = 'Harry Potter'
    search_input = request.args.get('search')

    sql = "SELECT id, title, poster_path " \
          "FROM movies_metadata " \
          "WHERE upper(title) like concat(upper(%s), '%')"
    cursor.execute(sql, (search_input.strip(),))
    rows = cursor.fetchall()

    # cursor.close()

     # each row
    result = []
    for row in rows:
        x = {}
        x['id'] = row[0]
        x['title'] = row[1]
        x['poster'] = row[2]
        result.append(x)
    # response = jsonify(dict(rows))
    print(result)
    response = jsonify(result)
    return response


# # Get user's rating history
@app.route('/moviesRating')
@cross_origin()
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

    # cursor.close()

    result = []
    for row in rows:
        x = {}
        x['id'] = row[0]
        x['title'] = row[1]
        x['poster'] = row[2]
        x['rating'] = row[3]
        result.append(x)
    # response = jsonify(dict(rows))
    print(rows)
    response = jsonify(result)
    return response


# Add/update user's new rating
@app.route('/movieRating', methods=['POST'])
@cross_origin()
def user_rating_upd():
    print('post rating update')
    print(request.headers['CONTENT_TYPE'])
    if request.headers['CONTENT_TYPE'] == 'application/json':
        print('post rating update get data')
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
        return 'Success'


# Get a list of recommended movies
@app.route('/movieSuggestion')
@cross_origin()
def movie_suggestion():
    # test
    # userid = 2103
    userid = request.args.get('userId')
    return ""
    # return movie_recommender(userid)


if __name__ == '__main__':
    app.run(debug=True)  # zijian
# app.run(port=5001)
