const express = require('express');
const app = express();

const bodyParser = require('body-parser');
const cors = require('cors');

app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());
app.use(cors());

let data = {
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
};

app.get('/movie',(req,res)=>{
    console.log(req.query);
    console.log(data.user_rating);
    if(parseInt(req.query.movieId) === data.id){
        res.send(data);
    }else{
        res.status(300).json({error:'movie not found'});
    }

});

app.post('/movieRating',(req,res)=>{
    // console.log(req.query.movieId);
    console.log(req.body);
    data.user_rating = parseInt(req.body.rating);
    console.log(data.user_rating);
});


let movieQuery = [
    {
        id:123,
        title:'HP4',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },
    {
        id:125,
        title:'HP5',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },{
        id:126,
        title:'HP6',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },{
        id:127,
        title:'Parites1',
        poster:'https://images-na.ssl-images-amazon.com/images/I/91hFpX7UCmL._SL1500_.jpg'
    },{
        id:128,
        title:'Parites2',
        poster:'https://images-na.ssl-images-amazon.com/images/I/91hFpX7UCmL._SL1500_.jpg'
    }
    ,{
        id:129,
        title:'HP7',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },{
        id:130,
        title:'HP1',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },{
        id:131,
        title:'HP2',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    },{
        id:132,
        title:'HP3',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg'
    }
];

app.get('/movieSearch',(req,res)=>{
    console.log(req.query);
    let search = req.query.search;
    let list = [];
    movieQuery.forEach(movie=>{
        if(movie.title.includes(search.toUpperCase())){
            list.push(movie);
        }
    });
    res.send(list);
});

app.get('/movieSuggestion',(req,res)=>{
    console.log(req.query);
    console.log('get suggestion request');
    res.send(movieQuery);
});

let ratingQuery = [
    {
        id:123,
        title:'HP4',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',
        rating:4
    },
    {
        id:125,
        title:'HP5',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',
        rating:4
    },{
        id:126,
        title:'HP6',
        poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',
        rating:3
    },{
        id:127,
        title:'Parites1',
        poster:'https://images-na.ssl-images-amazon.com/images/I/91hFpX7UCmL._SL1500_.jpg',
        rating:2
    }
];

app.get('/moviesRating',(req,res)=>{
    console.log(req.query);
    console.log('get rating record request');
    res.send(ratingQuery);
});

app.use((req,res,next)=>{
    const error = new Error('Not Found');
    error.status = 404;
    next(error);
});
module.exports = app;