# FancyMovieRecommendationSystem

## Install Tutorial
### For Frontend:   
Open console in front_end folder   
package install
```
npm install 
```
Run frontend
```
npm start
```
### For Backend:
Run database_query_table.sql in SQL   
Download rating_processed.csv file into data from https://drive.google.com/open?id=1y5f88zJIsDxsnxVRD1dykD9plU2xW2L1   
remember to change load file address     
```
LOAD DATA local INFILE  '[your location]\FancyMovieRecommendationSystem\data\cast_info.csv' INTO TABLE 
```
Open console in back_end folder   
Install package
```
pip install flask
pip install mysql_connector_python
```

You can change db user name and password in config.py

To generate recommended list for all old ratings:
```
python movie_recommender.py
```
It may take long time to run.   
   
Or you can generate certain user's recommend list:
```
python movie_recommendersingle_user.py [user id]
```
Run Backend:
```
python flash.py
```


## API  
### Search   
get a list of searched movies   
get localhost/movieSearch?search=${search}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    }   
]  

### Recommendation
get a list of recommended movies   
get localhost/movieSuggestion?userId=${userId}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
    }   
]  


### Rating Record
get a list of rated movies   
get localhost/moviesRating?userId=${userId}   
Return:   
[   
    {   
        id:123,   
        title:'HP4',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
        rating:3   
    },   
    {   
        id:125,   
        title:'HP5',   
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'   
        rating:4    
    }   
]  

### Update Rating Record
post a new movie rating   
post localhost/moviesRating   
Update:   
{   
    movieId: 123,   
    userId: test1,   
    rating:5   
}   
Return:   
Nothing in body   


### Movie Detail
post a movie detail information and user's rating   
get localhost/movie?movieId=123&userId='test1'  
Return:  
{   
    id:123,   
    title:'HP4',   
    genre:'Fantasy',   
    poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',   
    director:'Unknown',   
    actor:'Emma Watson',   
    avg_rating:4,   
    released:'2012',   
    description:'Harry Potter 4',    
    user_rating:4    
}   
