import React, {useState, useEffect}from 'react';
import axios from 'axios';
import '../bootstrap.css';
import '../App.css';
import logo from "../logo.svg"
import Rating from '@material-ui/lab/Rating';
import Box from '@material-ui/core/Box';
import {Link} from "react-router-dom";

const config=require('../config/default');

function Movie({match}) {
    const [movie,setMovie] = useState({
        title:'Test',
        genre:'',
        poster:logo,
        director:'',
        actor:'',
        avg_rating:3,
        released:'',
        description:'This is description',
        user_rating:-1
    });
    const [isLoad,setIsLoad] = useState(true);
    const [error,setError] = useState(null);
    const [rating,setRating] = useState(0);


    useEffect(()=>{
        console.log('effect Activate');
        getMovie();
    },[]);



    const getMovie = ()=>{
        axios.get(config.address+`/movie?` +
            `movieId=${match.params.id}` +
            `&userId=${localStorage.getItem("user_id")}`)
            .then(function (response) {
                // handle success
                setMovie(response.data);
                setRating(response.data.user_rating);
                setIsLoad(true);
                console.log(response.data.user_rating)
            })
            .catch(function (error) {
                // handle error
                console.log(error);
                setError(error);
                setIsLoad(true);
            })
    };

    const ratingUpdate = (newValue)=>{
        // console.log(typeof localStorage.getItem('access_token'));
        if (localStorage.getItem('access_token')==='true') {
            setRating(newValue);
            console.log('rating post');
            axios.post(config.address + `/movieRating`
                , {
                    movieId: match.params.id,
                    userId: localStorage.getItem("user_id"),
                    rating: newValue
                },{
                    headers: {
                        'Content-Type': 'application/json',
                        "Access-Control-Allow-Origin": "*",
                    }
                })
                .then(function (response) {
                    console.log(response);
                })
                .catch(function (error) {
                    console.log(error);
                });
        }else{
            setRating(null);
        }
    };

    if(error){
        console.log(error);
        return(
            <div>Error: {error.message}</div>
        );
    }else if(!isLoad){
        return <div>Loading...</div>;
    }else {
        return (
            <div>
                <div className="row">
                    <div className="col-md-4" >
                        <img src={'https://image.tmdb.org/t/p/original'+movie.poster} className="thumbnail" alt={"Poster"} />
                    </div>
                    <div className="col-md-8">
                        <h2 style={{marginBottom:'1em'}}>{movie.title}</h2>
                        <ul className="list-group">
                            <li className="list-group-item"><strong>Genre: </strong> {movie.genre}</li>
                            <li className="list-group-item"><strong>Released: </strong> {movie.released}</li>
                            <li className="list-group-item"><strong>IMDb Rating: </strong> {movie.avg_rating}</li>
                            <li className="list-group-item"><strong>Director: </strong> {movie.director}</li>
                            <li className="list-group-item"><strong>Actors: </strong> {movie.actor}</li>
                            <Box component="fieldset" mb={3} borderColor="transparent" style={{marginTop:'2em'}}>
                                <h4 style={{marginBottom:'1em'}}><strong>User Rating</strong></h4>
                                {
                                    localStorage.getItem('access_token')==='true'?<Rating
                                        name="simple-controlled"
                                        size="large"
                                        value={Math.max(rating,0)}
                                        onChange={(event, newValue) => {
                                            ratingUpdate(newValue);
                                        }}

                                    />:
                                    <Rating
                                    name="simple-controlled"
                                    size="large"
                                    value={0}
                                    disabled
                                    onChange={(event, newValue) => {
                                    ratingUpdate(newValue);
                                }}
                                    />
                                }
                            </Box>
                        </ul>
                    </div>
                </div>
                <div className="row">
                    <div className="well">
                        <p>
                            <h3>Description</h3>
                            {movie.description}
                        </p>
                    </div>
                </div>

                <div className="row">
                    <div className="well">
                        <Link to={`/`} className="btn btn-primary">
                            Go Back
                        </Link>
                    </div>
                </div>
            </div>
        );
    }
}

export default Movie;