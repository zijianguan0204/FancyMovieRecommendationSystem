# FancyMovieRecommendationSystem
- Data Import

  - File movies_metadata.csv -> Table [movies_metadata]
    1. Run script data_prep.py on the original csv file movies_metadata.csv, to generate movies_metadata_new.csv;
    2. Save and import (using correspinding part in movierecommender.sql)
    
Before testing, please make sure you have yoru database set up
For testing, please follow the steps
1. open one terminal go to back_end folder, then "python3/python flash.py"
2. open another terminal, go to front_end folder and then "npm install:, "npm start"
3. After the page pop up in your browser, change the URL to be : http://localhost:3000/movie/123, it is a testing page, you will see the Movie title as toystory has been passed to the front end and also the released date.

Until now, all connections are built, we can start query data from database to the front end.

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
