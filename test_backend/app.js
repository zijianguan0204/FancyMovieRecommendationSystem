const express = require('express');
const app = express();

const bodyParser = require('body-parser');
const cors = require('cors');

app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());
app.use(cors());

let data = {
    title:'HP4',
    genre:'Fantasy',
    poster:'https://images-na.ssl-images-amazon.com/images/I/517A4QTR22L._SY445_.jpg',
    director:'Unknown',
    actor:'Emma Watson',
    avg_rating:4,
    released:'2012',
    description:'Harry Potter 4',
    user_rating:-1
};

app.get('/movie',(req,res)=>{
    // console.log(req.query.movieId);
    console.log(data.user_rating);
   res.send(data);
});

app.post('/movieRating',(req,res)=>{
    // console.log(req.query.movieId);
    console.log(req.body);
    data.user_rating = parseInt(req.body.rating);
});

app.use((req,res,next)=>{
    const error = new Error('Not Found');
    error.status = 404;
    next(error);
});
module.exports = app;