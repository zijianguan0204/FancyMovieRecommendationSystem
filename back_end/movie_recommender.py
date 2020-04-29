import datetime
import mysql.connector
from datetime import timedelta, date
from flask import Flask, render_template, request, json, jsonify
from mysql.connector import Error

password = ''

def movie_recommender(userid):
    try:
        connection_suggestion = mysql.connector.connect(host='localhost',
                                         database='movie_Recommender',
                                         user='root',
                                         password=password) #zijian
                                        #  auth_plugin='mysql_native_password', # V
                                        #  password='leoJ0205') # V
        if connection_suggestion.is_connected():
            db_Info_suggestion = connection_suggestion.get_server_info()
            cursor_suggestion = connection_suggestion.cursor()
            print("Connected to MySQL Server version ", db_Info_suggestion)

    except Error as e:
        print("Error while connecting to MySQL", e)

    userid = request.args.get('userId')
#userid = 1
    print(userid)
    var_list = [0.4, 0.2, 0.3, 0.05, 0.05]

# get all movie Id that the user rated >=4 into list
    sql = "SELECT movieId FROM movie_Recommender.ratings WHERE userid = %s AND rating >= 4"
    cursor_suggestion.execute(sql,(userid,))
    rows = cursor_suggestion.fetchall()
    movieid_list = []
    for tup in rows:
        movieid_list.append(tup[0])

# get all movie rated within 14 days into list
    recent_list = []
    for movieid in movieid_list:
        sql = "SELECT timestamp FROM movie_Recommender.ratings WHERE userid = %s AND movieid = %s"
        cursor_suggestion.execute(sql,(userid, movieid,))
        rows = cursor_suggestion.fetchall()
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
        cursor_suggestion.execute(sql,(userid, ts,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            final_movie_list.append(tup[0])

# add movie in the same collection into the recommend/unrecommend list
    recommend_list = []
    unrecommend_list = []
    collection_list = []
    for movieid in movieid_list:
        sql = "SELECT collection FROM movie_Recommender.movies_metadata WHERE id = %s"
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            if tup[0] > 0:
                collection_list.append(tup[0])

    for collection_id in collection_list:
        sql = "SELECT id FROM movie_Recommender.movies_metadata WHERE collection = %s"
        cursor_suggestion.execute(sql,(collection_id,))
        rows = cursor_suggestion.fetchall()
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
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
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
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
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
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
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
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            if '>=2000' in releaseDate_dict:
                releaseDate_dict['>=2000'] += 1
            else:
                releaseDate_dict['>=2000'] = 1

        sql = "SELECT release_date FROM movies_metadata WHERE release_date < '2000' AND id = %s"
        cursor_suggestion.execute(sql,(movieid,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            if '<2000' in releaseDate_dict:
                releaseDate_dict['<2000'] += 1
            else:
                releaseDate_dict['<2000'] = 1
    total_dict.update(releaseDate_dict)

    # get top 15 tags
    top_tags = []
    for k in sorted(total_dict, key=total_dict.get, reverse=True):
        top_tags.append(k)
    if len(top_tags) > 15:
        top_tags = top_tags[0:14]


    #insert to recommend_list
    userId = 1
    movie_list = ['1','2','3','4','5']
    recommend_movie = ''
    for movie in movie_list:
        recommend_movie = recommend_movie + ',' + movie
    sql = "INSERT INTO recommend_list (userid, movie_list) VALUES(%s, %s) ON DUPLICATE KEY UPDATE userid = %s;"
    try:
        cursor.execute(sql,(userId,recommend_movie,))
        connection.commit()
        print("successfully executed sql in recommend_movie")
    except Error as e:
        print("Error while executing SQL in recommend movie", e)
    



    response = jsonify(data = [])
    return None
