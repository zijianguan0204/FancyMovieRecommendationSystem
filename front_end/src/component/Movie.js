import React, {useState, useEffect}from 'react';
import axios from 'axios';
import '../bootstrap.css';
import '../App.css';
import logo from "../logo.svg"
import Rating from '@material-ui/lab/Rating';
import Box from '@material-ui/core/Box';

function Movie({match}) {
    useEffect(()=>{
        getMovie();
        console.log(movie)
    });

    const [movie,setMovie] = useState({
        title:'Test',
        genre:'',
        poster:logo,
        director:'',
        actor:'',
        avg_rating:3,
        released:'',
        description:'Lalalalalala',
        user_rating:-1
    });
    const [isLoad,setIsLoad] = useState(true);
    const [error,setError] = useState(null);

    const fetchMovie = ()=>{
        let addr = `https://ec2-3-101-24-190.us-west-1.compute.amazonaws.com`;
        fetch(
            `http://localhost:5000/movie?` +
            `movieId=${match.params.id}` +
            `&userId=${localStorage.getItem("user_id")}`
        ).then(res=>res.json())
            .then(
                (res)=>{
                    setMovie(res);
                    setIsLoad(true)
                },
                (err)=>{
                    // setError(err);
                    setIsLoad(true)
                }
            )
    };

    const getMovie = ()=>{
        axios.get(`http://localhost:5000/movie?` +
            `movieId=${match.params.id}` +
            `&userId=${localStorage.getItem("user_id")}`)
            .then(function (response) {
                // handle success
                console.log(response);
                setMovie(response.data);
                setIsLoad(true)
            })
            .catch(function (error) {
                // handle error
                console.log(error);
                setIsLoad(true);
            })
    };

    const ratingUpdate = (rating)=>{
        axios.post(`http://localhost:5000/movieRating`
            , {
                movieId: match.params.id,
                userId: localStorage.getItem("user_id"),
                rating:rating
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    if(error){
        console.log(error);
        return(
            <div>Error: {error.message}</div>
        );
    }else if(!isLoad){
        return <div>Loading...</div>;
    }else {
        console.log(movie);
        return (
            <div>
                <div className="row">
                    <div className="col-md-4" >
                        <img src={movie.poster} className="thumbnail" alt={"Poster"} />
                    </div>
                    <div className="col-md-8">
                        <h2 style={{marginBottom:'1em'}}>{movie.title}</h2>
                        <ul className="list-group">
                            <li className="list-group-item"><strong>Genre: </strong> {movie.genre}</li>
                            <li className="list-group-item"><strong>Released: </strong> {movie.released}</li>
                            <li className="list-group-item"><strong>Rated: </strong> {movie.avg_rating}</li>
                            <li className="list-group-item"><strong>Director: </strong> {movie.director}</li>
                            <li className="list-group-item"><strong>Actors: </strong> {movie.actor}</li>
                            <Box component="fieldset" mb={3} borderColor="transparent" style={{marginTop:'2em'}}>
                                <li style={{marginBottom:'1em'}}><strong>User Rating</strong></li>
                                <Rating
                                    name="simple-controlled"
                                    size="large"
                                    value={Math.max(movie.user_rating,0)}
                                    onChange={(event, newValue) => {
                                        ratingUpdate(newValue);
                                    }}
                                />
                            </Box>
                        </ul>
                    </div>
                </div>
                <div className="row">
                    <div className="well">
                        <h3>Description</h3>
                        {movie.description}
                    </div>
                </div>

                <div className="row">
                    <div className="well">
                        <a href="/" className="btn btn-primary">View
                            Go Back
                        </a>
                    </div>
                </div>
            </div>
        );
    }
}

export default Movie;