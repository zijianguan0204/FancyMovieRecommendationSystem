import mysql.connector
from mysql.connector import Error

password = ''


class MovieStatistics:
    def __init__(self):
        """
        initialize sql connector
        retrieve all required genre, cast, crew count from database
        """
        self.__total = {}
        try:
            self.__connection_suggestion = mysql.connector.connect(host='localhost',
                                                                   database='movie_Recommender',
                                                                   user='root',
                                                                   password=password)  # zijian
            #  auth_plugin='mysql_native_password', # V
            #  password='leoJ0205') # V
            if self.__connection_suggestion.is_connected():
                self.__db_Info_suggestion = self.__connection_suggestion.get_server_info()
                self.__cursor_suggestion = self.__connection_suggestion.cursor()
                print("Movie Statistics Connected to MySQL Server version ", self.__db_Info_suggestion)

        except Error as e:
            print("Error while connecting to MySQL", e)

        self.__genre_count = {}
        sql = "SELECT genre,count(id) FROM movie_Recommender.movie_genre " \
              "GROUP BY genre "
        self.__cursor_suggestion.execute(sql)
        rows = self.__cursor_suggestion.fetchall()
        for tup in rows:
            self.__genre_count[tup[0]] = tup[1]
        self.__total.update(self.__genre_count)

        self.__cast_count = {}
        sql = "SELECT name,count(movie_id) FROM movie_Recommender.movie_cast INNER JOIN movie_Recommender.cast_infor " \
              "WHERE cast_id = id " \
              "GROUP BY cast_id "
        self.__cursor_suggestion.execute(sql)
        rows = self.__cursor_suggestion.fetchall()
        for tup in rows:
            self.__cast_count[tup[0]] = tup[1]
        self.__total.update(self.__cast_count)

        self.__director_count = {}
        sql = "SELECT name,count(movie_id) FROM movie_Recommender.movie_crew INNER JOIN movie_Recommender.crew_info " \
              "WHERE crew_id = id AND job = 'Director'" \
              "GROUP BY crew_id "
        self.__cursor_suggestion.execute(sql)
        rows = self.__cursor_suggestion.fetchall()
        for tup in rows:
            self.__director_count[tup[0]] = tup[1]
        self.__total.update(self.__director_count)

        self.__connection_suggestion.close()

    def get_director(self):
        return self.__director_count

    def get_cast(self):
        return self.__cast_count

    def get_genre(self):
        return self.__genre_count

    def get_total(self):
        return self.__total

#
# if __name__ == "__main__":
#     m = MovieStatistics()
#     print(m.get_cast())
#     print(m.get_director())
#     print(m.get_genre())
