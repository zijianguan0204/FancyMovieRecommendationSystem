import datetime
import mysql.connector
from datetime import timedelta
from movie_statistics import MovieStatistics
from mysql.connector import Error
import time
import math
from collections import defaultdict

password = ''


def movie_recommend_update(userid, movie_statistics):
    """
    get a new recommendation list for user
    :param userid: user's id who looking for new recommendation list
    :param movie_statistics:  MovieStatistics object
    :return:recommendation movie id list
    """
    try:
        connection_suggestion = mysql.connector.connect(host='localhost',
                                                        database='movie_Recommender',
                                                        user='root',
                                                        password=password)  # zijian
        #  auth_plugin='mysql_native_password', # V
        #  password='leoJ0205') # V
        if connection_suggestion.is_connected():
            db_Info_suggestion = connection_suggestion.get_server_info()
            cursor_suggestion = connection_suggestion.cursor()
            print("Connected to MySQL Server version ", db_Info_suggestion)

    except Error as e:
        print("Error while connecting to MySQL", e)

    print(userid)
    start = time.time()
    recommend_list = []
    default_recommend_list = []
    unrecommend_list = []


    #get the first 20 most popular movies as the default list
    sql = "SELECT movieId FROM movie_Recommender.movies_metadata ORDER BY popularity DESC;"
    cursor_suggestion.execute(sql, (userid,))
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        default_recommend_list.append(tup[0])
    default_recommend_list = default_recommend_list[0:19]

    # get all movie Id that the user rated >=4 into list
    sql = "SELECT movieId,timestamp,rating FROM movie_Recommender.ratings WHERE userid = %s AND rating >= 4"
    cursor_suggestion.execute(sql, (userid,))
    rows = cursor_suggestion.fetchall()
    #if the user is new, he has not rated any movie, recommend default
    if len(rows) == 0:
        return default_recommend_list

    movieid_list = []
    movie_rating = {}
    movie_rating_timestamp = {}
    for tup in rows:
        movie_rating[tup[0]] = int(tup[2])
        movieid_list.append(tup[0])
        movie_rating_timestamp[tup[0]] = float(tup[1])
    max_timestamp = datetime.datetime.fromtimestamp(float(max(movie_rating_timestamp.values())))
    movie_rating_parameter = {}
    for key, val in movie_rating_timestamp.items():
        temp_timestamp = datetime.datetime.fromtimestamp(float(val))
        movie_rating_parameter[key] = time_variance(temp_timestamp, max_timestamp)

    # get all movie rated within 14 days into list
    recent_list = []
    for movieid in movieid_list:
        sql = "SELECT timestamp FROM movie_Recommender.ratings WHERE userid = %s AND movieid = %s"
        cursor_suggestion.execute(sql, (userid, movieid,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            cur_ts = tup[0] + '000'
            recent_list.append(cur_ts)

    recent_list.sort(reverse=True)
    if recent_list:
        most_recent_ts = recent_list[0]
        most_recent_date = datetime.datetime.fromtimestamp(float(most_recent_ts) / 1e3)
        date_before_14days = most_recent_date - timedelta(days=14)
        ts_before_14days = int(datetime.datetime.timestamp(date_before_14days))

    ts_list = []
    for ts in recent_list:
        if int(ts) >= ts_before_14days:
            ts_list.append(ts)

    final_movie_list = []
    for ts in ts_list:
        ts = str(int(ts) // 1000)
        # ts = ts + "\r"
        sql = "SELECT movieid FROM movie_Recommender.ratings WHERE userid = %s AND timestamp = %s"
        cursor_suggestion.execute(sql, (userid, ts,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            final_movie_list.append(tup[0])

    # add movie in the same collection into the recommend/unrecommend list

    collection_list = []
    for movieid in movieid_list:
        sql = "SELECT collection FROM movie_Recommender.movies_metadata WHERE id = %s"
        cursor_suggestion.execute(sql, (movieid,))
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            if tup[0] > 0:
                collection_list.append(tup[0])

    for collection_id in collection_list:
        sql = "SELECT id FROM movie_Recommender.movies_metadata WHERE collection = %s"
        cursor_suggestion.execute(sql, (collection_id,))
        rows = cursor_suggestion.fetchall()
        count = 0
        for tup in rows:
            if count == 0:
                recommend_list.append(tup[0])
                count += 1
            else:
                unrecommend_list.append(tup[0])
    print("Movie collection retrieve", time.time() - start)
    #

    movieid_list_sql = '(' + ','.join(map(str, movieid_list)) + ')'
    # create a total dictionary
    total_dict = {}
    movie_rated_tag = defaultdict(set)
    # get all genres into dictionary
    genre_dict = defaultdict(float)
    sql = "SELECT id, genre FROM movie_Recommender.movie_genre " \
          "WHERE id in %s" % movieid_list_sql
    cursor_suggestion.execute(sql)
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        genre_dict[tup[1]] += (movie_rating[tup[0]]-3) * movie_rating_parameter[tup[0]]
        movie_rated_tag[tup[0]].add(tup[1])

    total_dict.update(genre_dict)
    print("Movie genre retrieve", time.time() - start)

    # get all cast into dictionary
    cast_dict = defaultdict(float)
    sql = "SELECT movie_id,name FROM movie_Recommender.movie_cast INNER JOIN movie_Recommender.cast_infor " \
          "WHERE cast_id = id AND movie_id in %s" % movieid_list_sql
    cursor_suggestion.execute(sql)
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        cast_dict[tup[1]] += (movie_rating[tup[0]]-3) * movie_rating_parameter[tup[0]]
        movie_rated_tag[tup[0]].add(tup[1])
    total_dict.update(cast_dict)
    print("Movie cast retrieve", time.time() - start)

    # get all director into dictionary
    director_dict = defaultdict(float)
    sql = "SELECT movie_id,name FROM movie_Recommender.movie_crew INNER JOIN movie_Recommender.crew_info " \
          "WHERE crew_id = id AND job = 'Director' AND movie_id in %s " % movieid_list_sql
    cursor_suggestion.execute(sql)
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        director_dict[tup[1]] += (movie_rating[tup[0]]-3) * movie_rating_parameter[tup[0]]
        movie_rated_tag[tup[0]].add(tup[1])
    total_dict.update(director_dict)
    print("Movie crew retrieve", time.time() - start)

    # get all release_date into dictionary
    # releaseDate_dict = defaultdict(float)
    # # for movieid in movieid_list:
    # sql = "SELECT id,release_date FROM movies_metadata " \
    #       "WHERE release_date >= '2000' AND id in %s" % movieid_list_sql
    # cursor_suggestion.execute(sql)
    # rows = cursor_suggestion.fetchall()
    # for tup in rows:
    #     releaseDate_dict['>=2000'] += 1 * movie_rating_parameter[tup[0]]
    #
    # sql = "SELECT id,release_date FROM movies_metadata " \
    #       "WHERE release_date < '2000' AND id in %s" % movieid_list_sql
    # cursor_suggestion.execute(sql)
    # rows = cursor_suggestion.fetchall()
    # for tup in rows:
    #     releaseDate_dict['<2000'] += 1 * movie_rating_parameter[tup[0]]
    # # total_dict.update(releaseDate_dict)
    # print("Movie release retrieve", time.time() - start)

    # get top 15 tags
    top_tags = []
    for k, val in sorted(total_dict.items(), key=lambda x: x[1], reverse=True):
        top_tags.append((k, val))
    if len(top_tags) > 15:
        top_tags = top_tags[0:14]
    print(top_tags)
    print("Movie tag retrive", time.time() - start)
    # response = jsonify(data = [])

    # Create candidate list
    candidate = defaultdict(set)

    # get genre candidate
    genre_list = list(set(genre_dict.keys()) & set(map(lambda x: x[0], top_tags)))
    if genre_list:
        sql = "SELECT id, genre FROM movie_Recommender.movie_genre " \
              "WHERE genre in %s" % '(' + ','.join(map(lambda x: "'" + x + "'", genre_list)) + ')'
        cursor_suggestion.execute(sql)
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            candidate[tup[0]].add(tup[1])

    # get cast candidate
    cast_list = list(set(cast_dict.keys()) & set(map(lambda x: x[0], top_tags)))
    if cast_list:
        sql = "SELECT movie_id,name FROM movie_Recommender.movie_cast INNER JOIN movie_Recommender.cast_infor " \
              "WHERE cast_id = id AND name in %s" % '(' + ','.join(map(lambda x: "'" + x + "'", cast_list)) + ')'
        cursor_suggestion.execute(sql)
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            candidate[tup[0]].add(tup[1])

    # get director candidate
    director_list = list(set(director_dict.keys()) & set(map(lambda x: x[0], top_tags)))
    if director_list:
        sql = "SELECT movie_id,name FROM movie_Recommender.movie_crew INNER JOIN movie_Recommender.crew_info " \
              "WHERE crew_id = id AND job = 'Director' " \
              "AND name in %s " % '(' + ','.join(map(lambda x: "'" + x + "'", director_list)) + ')'

        cursor_suggestion.execute(sql)
        rows = cursor_suggestion.fetchall()
        for tup in rows:
            candidate[tup[0]].add(tup[1])

    print("candidate retrieve", time.time() - start)

    # Algorithm start
    count = 0
    recommend_candidate = {}
    for _movie_id, _movie_set in sorted(candidate.items(), key=lambda x: len(x[1]), reverse=True):
        if count >= 50 and len(_movie_set) <= 2:
            break
        if len(recommend_list) > 20:
            break
        if count >= 1000:
            break
        _numerator = 0.0
        _denominator = 0.0

        # Calculate TF-IDF based on all rated movie tags
        for _movie_rated_id, _movie_rated_tag in movie_rated_tag.items():
            common = _movie_set & _movie_rated_tag
            tfidf = 0.0
            for _tag in common:
                try:
                    tfidf += total_dict[_tag] / math.log(movie_statistics.get_total()[_tag])
                except ZeroDivisionError:
                    continue
            _numerator += tfidf * int(movie_rating[_movie_rated_id])
            _denominator += tfidf
        if _denominator == 0:
            continue
        # calculate predicted rating
        if _numerator / _denominator > 4.5:
            recommend_list.append(_movie_id)
            # print(count, _movie_id, _numerator / _denominator)
        elif _numerator / _denominator > 3.5:
            recommend_candidate[_movie_id] = _numerator / _denominator
        count += 1
        # print(_movie_id, _movie_set)

    for _movie_id, _ in sorted(recommend_candidate.items(), key=lambda x: x[1], reverse=True):
        if len(recommend_list) > 20:
            break
        recommend_list.append(_movie_id)
    print("recommend_list",recommend_list)

    # adding list to db
    str_recommend_list = ','.join(map(str,recommend_list))
    sql = "INSERT INTO recommend_list (userid, movie_list) VALUES(%s, %s) ON DUPLICATE KEY UPDATE userid = %s;"
    try:
        cursor.execute(sql,(userId,str_recommend_list,))
        connection.commit()
        print("successfully executed sql")
    except Error as e:
        print("Error while executing SQL", e)

    return recommend_list


def time_variance(this_time, last_time=datetime.datetime.now()):
    """
    Introduce time variance to tag count
    :param this_time: time when rating made
    :param last_time: time when last rating made
    :return: coefficient for tag calculating
    """
    day = (last_time - this_time).days
    return min(math.exp((-day + 14) / 320), 1)


if __name__ == "__main__":
    m = MovieStatistics()
    movie_recommend_update(7896, m)

