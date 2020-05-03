from flask import Flask, render_template, request, json, jsonify

import mysql.connector
import ast
import random
from flask_cors import cross_origin
from mysql.connector import Error
import json
from movie_recommender import movie_recommend_update
from movie_statistics import MovieStatistics
import datetime

app = Flask(__name__)

password = ''

print("Backend Start")
m = MovieStatistics()

# Connect to Database
try:
    connection = mysql.connector.connect(host='localhost',
                                         database='movie_Recommender',
                                         user='root',
                                         password=password)

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Flask Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()

except Error as e:
    print("Error while connecting to MySQL", e)

try:
    connection2 = mysql.connector.connect(host='localhost',
                                          database='movie_Recommender',
                                          user='root',
                                          password=password)  # zijian
    #  auth_plugin='mysql_native_password', # V
    #  password='leoJ0205') # V
    if connection2.is_connected():
        db_Info = connection2.get_server_info()
        print("Flask Connected to MySQL Server version ", db_Info)
        cursor2 = connection2.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)

try:
    connection3 = mysql.connector.connect(host='localhost',
                                          database='movie_Recommender',
                                          user='root',
                                          password=password)  # zijian
    #  auth_plugin='mysql_native_password', # V
    #  password='leoJ0205') # V
    if connection3.is_connected():
        db_Info = connection3.get_server_info()
        print("Flask Connected to MySQL Server version ", db_Info)
        cursor3 = connection3.cursor()
except Error as e:
    print("Error while connecting to MySQL", e)

print("SQL Established")


# Get movie detail according to movie ID and user ID
@app.route('/movie')
@cross_origin()
def movie():
    movieId = request.args.get('movieId')
    userId = request.args.get('userId')

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
    tag = ''
    taste_set = set()
    common_test = set()
    user_rating = -1

    # get user tag
    if userId != 'null':
        sql = "SELECT tag FROM movie_recommender.recommend_list WHERE userid = %s"
        cursor.execute(sql, (int(userId),))
        tag_dr = cursor.fetchall()
        if tag_dr:
            print(tag_dr)
            taste_set = set(tag_dr[0][0].split(','))
        print("taste_set", taste_set)

        # get user rating
        sql = "SELECT rating " \
              "FROM ratings " \
              "WHERE movieid = %s " \
              "AND userid = %s"
        cursor.execute(sql, (movieId, int(userId),))
        user_rating_dr = cursor.fetchone()
        user_rating = None if (user_rating_dr == None) else user_rating_dr[0]

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
    if genres_dr:
        genres_str = ','.join(map(lambda x: x[0], genres_dr))
        common_test |= set(map(lambda x: x[0], genres_dr)) & taste_set
        print(taste_set,set(map(lambda x: x[0], genres_dr)))

    # get actors (cast)
    sql = "SELECT cast_infor.name " \
          "FROM movie_Recommender.cast_infor " \
          "INNER JOIN movie_cast " \
          "ON cast_infor.id = movie_cast.cast_id " \
          "WHERE movie_id = %s"
    cursor.execute(sql, (int(movieId),))
    actors_dr = cursor.fetchall()
    if actors_dr:
        actors_str = ','.join(map(lambda x: x[0], actors_dr))
        common_test |= set(map(lambda x: x[0], actors_dr)) & taste_set

    # get director (crew)
    sql = "SELECT name " \
          "FROM crew_info " \
          "INNER JOIN movie_crew " \
          "ON crew_info.id = movie_crew.crew_id " \
          "WHERE movie_id = %s " \
          "AND job = 'director'"
    cursor.execute(sql, (int(movieId),))
    director_dr = cursor.fetchall()
    if director_dr:
        director_str = ','.join(map(lambda x: x[0], director_dr))
        common_test |= set(map(lambda x: x[0], director_dr)) & taste_set

    if common_test:
        print('Movie common taste', common_test)
        tag = ','.join(list(common_test))

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
        'user_rating': user_rating,
        'tag': tag
    }

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
    # print(result)

    response = jsonify(result)
    return response


# # Get user's rating history
@app.route('/moviesRating')
@cross_origin()
def user_rating_history():
    # test
    # userid = 2103
    try:
        userid = int(request.args.get('userId'))
    except ValueError:
        return ''

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
        print(movieId)
        userId = int(request.json['userId'])
        rating = request.json['rating']
        current = datetime.datetime.now()
        cur_date_obj = datetime.datetime(current.year, current.month, current.day)
        timestamp = int(datetime.datetime.timestamp(cur_date_obj))

        sql = "INSERT INTO ratings (userid, movieid, rating, timestamp) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE rating = %s, timestamp = %s;"
        try:
            cursor.execute(sql, (userId, movieId, rating, timestamp, rating, timestamp,))
            connection.commit()
            print("successfully executed sql")
        except Error as e:
            print("Error while executing SQL", e)

        rec_movie_list = movie_recommend_update(userId, m)
        # # adding list to db
        # str_recommend_list = ','.join(map(str,rec_movie_list))
        # sql = "INSERT INTO recommend_list (userid, movie_list) VALUES(%s, %s) ON DUPLICATE KEY UPDATE userid = %s;"
        # try:
        # 	cursor.execute(sql,(userId,str_recommend_list,userId,))
        # 	connection.commit()
        # 	print("successfully executed sql")
        # except Error as e:
        # 	print("Error while executing SQL", e)

        response = jsonify("")
        return 'Success'


# Get a list of recommended movies
@app.route('/movieSuggestion')
@cross_origin()
def movie_suggestion():
    userid = request.args.get('userId')
    sql = "SELECT movie_list FROM movie_recommender.recommend_list where userid = %s" % userid
    print(userid)
    rows = []
    try:
        cursor2.execute(sql)
        rows = cursor2.fetchall()
        print("successfully executed sql", rows)
    except Error as e:
        print("Error while executing SQL", e)

    result = []
    rec_list = ''
    rec_mov_list = []

    if not rows or len(rows) == 0:
        rec_mov_list = movie_recommend_update(userid, m)
        movieid_list_sql = '(' + ','.join(map(str, rec_mov_list)) + ')'
    else:
        for tup in rows:
            rec_list = tup[0]
        rec_str = rec_list.split(",")
        for movie in rec_str:
            rec_mov_list.append(int(movie))
    movieid_list_sql = '(' + ','.join(map(str, rec_mov_list)) + ')'
    print('retrieve movie list', movieid_list_sql)
    sql = "SELECT id, title, poster_path FROM movies_metadata WHERE id in %s" % movieid_list_sql
    cursor2.execute(sql)
    rows = cursor2.fetchall()
    for row in rows:
        x = {}
        x['id'] = row[0]
        x['title'] = row[1]
        x['poster'] = row[2]
        result.append(x)

    # print(result)

    result = random.sample(result, 8)
    print("Here is the final recommended result")
    print(result)
    response = jsonify(result)
    return response
    # return ""
    # return movie_recommender(userid)


if __name__ == '__main__':
    app.run(debug=True)  # zijian
# app.run(port=5001)
