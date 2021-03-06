import datetime
import mysql.connector
from datetime import timedelta
from movie_statistics import MovieStatistics
from mysql.connector import Error
import time
import math
from collections import defaultdict
import config



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
                                                        user=config.user,
                                                        password=config.password)  # zijian
        #  auth_plugin='mysql_native_password', # V
        #  password='leoJ0205') # V
        if connection_suggestion.is_connected():
            db_Info_suggestion = connection_suggestion.get_server_info()
            cursor_suggestion = connection_suggestion.cursor()
            print("Movie Recommender Connected to MySQL Server version ", db_Info_suggestion)

    except Error as e:
        print("Error while connecting to MySQL", e)

    print('user id', userid)
    start = time.time()
    recommend_list = []
    default_recommend_list = []
    unrecommend_list = []

    # get the first 20 most popular movies as the default list
    sql = "SELECT id FROM movie_Recommender.movies_metadata ORDER BY popularity DESC;"
    cursor_suggestion.execute(sql)
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        default_recommend_list.append(tup[0])
    default_recommend_list = default_recommend_list[0:19]

    if not userid:
        return default_recommend_list, set()

    # get all movie Id that the user rated >=4 into list
    sql = "SELECT movieId,timestamp,rating FROM movie_Recommender.ratings WHERE userid = %s AND rating >= 4"
    cursor_suggestion.execute(sql, (userid,))
    rows = cursor_suggestion.fetchall()
    # if the user is new, he has not rated any movie, recommend default
    if len(rows) <= 1:
        str_recommend_list = ','.join(map(str, default_recommend_list))
        sql = "INSERT INTO recommend_list (userid, movie_list) VALUES(%s, %s) ON DUPLICATE KEY UPDATE movie_list = %s;"
        try:
            cursor_suggestion.execute(sql, (userid, str_recommend_list, str_recommend_list,))
            connection_suggestion.commit()
            print("successfully insert data as default list")
        except Error as e:
            print("Error while executing SQL doing default list", e)
        print('Return Default Recommend List')
        return default_recommend_list, set()

    movieid_list = []
    movie_rating = {}
    movie_rating_timestamp = {}
    for tup in rows:
        movie_rating[tup[0]] = int(tup[2])
        movieid_list.append(tup[0])
        movie_rating_timestamp[tup[0]] = float(tup[1])
        unrecommend_list.append(tup[0])
    max_timestamp = datetime.datetime.fromtimestamp(float(max(movie_rating_timestamp.values())))
    movie_rating_parameter = {}
    for key, val in movie_rating_timestamp.items():
        temp_timestamp = datetime.datetime.fromtimestamp(float(val))
        movie_rating_parameter[key] = time_variance(temp_timestamp, max_timestamp)

    # Remove all low rating movies
    sql = "SELECT movieId FROM movie_Recommender.ratings WHERE userid = %s AND rating <= 3"
    cursor_suggestion.execute(sql, (userid,))
    rows = cursor_suggestion.fetchall()
    for tup in rows:
        unrecommend_list.append(tup[0])

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
    for movieid in final_movie_list:
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
            if count == 0 and tup[0] != collection_id and tup[0] not in unrecommend_list:
                if tup[0] not in recommend_list:
                    recommend_list.append(tup[0])
                    count += 1
            else:
                unrecommend_list.append(tup[0])
    print("Movie collection retrieve", time.time() - start)
    print("here is the recommend list after collection")
    print(recommend_list)
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

    # print("tup is below ")
    for tup in rows:
        # print(tup)
        genre_dict[tup[1]] += ((movie_rating[tup[0]] - 3) * movie_rating_parameter[tup[0]])
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
        cast_dict[tup[1]] += ((movie_rating[tup[0]] - 3) * movie_rating_parameter[tup[0]])
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
        director_dict[tup[1]] += ((movie_rating[tup[0]] - 3) * movie_rating_parameter[tup[0]])
        movie_rated_tag[tup[0]].add(tup[1])
    total_dict.update(director_dict)

    # get top 15 tags
    top_tags = []
    try:
        tag_max = max(total_dict.values())
    except ValueError:
        return default_recommend_list, set()
    for k, val in sorted(total_dict.items(), key=lambda x: x[1], reverse=True):
        # print('tag', k, val)
        if val >= 2 or tag_max <= 2 and val > 1:
            top_tags.append((k, val))
    n = 15
    if len(top_tags) > n:
        top_tags = top_tags[0:n]
    elif len(top_tags) < 2:
        print('tag list is too short to record, return default list', top_tags)
        return default_recommend_list, set()

    tag_score = {}
    for tup in top_tags:
        tag_score[tup[0]] = tup[1]

    print("Movie tag retrive", time.time() - start)
    print("below is the top_tags")
    print(top_tags)

    if not top_tags:
        return default_recommend_list, set()

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
    print("num of candidate", len(candidate))

    # Algorithm start
    count = 0
    recommend_candidate = {}
    tag_check = defaultdict(float)
    movie_predict = {}
    waiting_list = defaultdict(list)
    for _movie_id, _movie_set in sorted(candidate.items(), key=lambda x: len(x[1]), reverse=True):
        if count >= 100 and len(_movie_set) <= 2:
            break
        if count >= 1000:
            break
        _numerator = 0.0
        _denominator = 0.0

        if _movie_id in unrecommend_list:
            continue

        # Calculate TF-IDF based on all rated movie tags
        for _movie_rated_id, _movie_rated_tag in movie_rated_tag.items():
            common = _movie_set & _movie_rated_tag
            tfidf = 0.0
            for _tag in common:
                try:
                    tfidf += total_dict[_tag] / math.log(movie_statistics.get_total()[_tag])
                    tag_check[_tag] = total_dict[_tag] / math.log(movie_statistics.get_total()[_tag])
                except ZeroDivisionError:
                    continue
            _numerator += tfidf * int(movie_rating[_movie_rated_id])
            _denominator += tfidf
        if _denominator == 0:
            continue

        # calculate predicted rating
        if _numerator / _denominator >= 4:
            score = 0
            for tag in _movie_set:
                score += tag_check[tag]
            waiting_list[round(_numerator / _denominator, 1)].append((_movie_id, score))
        count += 1
    # print('waiting_list', waiting_list)
    for _, _movie_list in sorted(waiting_list.items(), key=lambda x: x[0], reverse=True):
        # print('movie estimate rating',_)
        if len(recommend_list) > 20:
            break

        for (_movie_id, _) in sorted(_movie_list, key=lambda x: x[1], reverse=True):
            # print('Movie Score', _movie_id,_)
            if len(recommend_list) > 20:
                break
            recommend_list.append(_movie_id)

    print("recommend_list", recommend_list)

    print('tag check', tag_check)

    final_recommend_list = []
    for movie in recommend_list:
        if movie not in movieid_list:
            final_recommend_list.append(movie)

    final_recommend_list = set(final_recommend_list)

    unrecommend_list = set(unrecommend_list)
    print(final_recommend_list)
    print(unrecommend_list)
    # print("here is the recommend list before remove from unrecommend")
    # print(recommend_list)

    final_recommend_list = final_recommend_list - unrecommend_list
    # print("here is the recommend list after remove from unrecommend")
    # print(recommend_list)

    # adding list to db
    str_recommend_list = ','.join(map(str, final_recommend_list))
    sql = "INSERT INTO recommend_list (userid, movie_list,tag) VALUES(%s, %s, %s) " \
          "ON DUPLICATE KEY UPDATE movie_list = %s, tag = %s;"
    try:
        cursor_suggestion.execute(sql, (
            userid, str_recommend_list, ','.join(map(lambda x: x[0], top_tags)), str_recommend_list,
            ','.join(map(lambda x: x[0], top_tags))))
        connection_suggestion.commit()
        print("successfully insert data")
    except Error as e:
        print("Error while executing SQL", e)
    connection_suggestion.close()

    return final_recommend_list, set(map(lambda x: x[0], top_tags))


def time_variance(this_time, last_time=datetime.datetime.now()):
    """
    Introduce time variance to tag count
    :param this_time: time when rating made
    :param last_time: time when last rating made
    :return: coefficient for tag calculating
    """
    day = (last_time - this_time).days
    return min(math.exp((-day + 14) / 320), 1)


#
if __name__ == "__main__":
    try:
        m = MovieStatistics()
        movie_recommend_update(int(sys.argv[1]), m)
    except Exception:
        print(Exception)
