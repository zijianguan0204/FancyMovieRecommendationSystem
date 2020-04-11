import React, {useState, useEffect}from 'react';
import '../bootstrap.css';
import '../App.css';
import logo from "../logo.svg"

function Movie({match}) {
    useEffect(()=>{
        fetchMovie();
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
        fetch(
            `https://ec2-3-101-24-190.us-west-1.compute.amazonaws.com/movie?` +
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
                        <h2>{movie.title}</h2>
                        <ul className="list-group">
                            <li className="list-group-item"><strong>Genre: </strong> {movie.genre}</li>
                            <li className="list-group-item"><strong>Released: </strong> {movie.released}</li>
                            <li className="list-group-item"><strong>Rated: </strong> {movie.avg_rating}</li>
                            <li className="list-group-item"><strong>Director: </strong> {movie.director}</li>
                            <li className="list-group-item"><strong>Actors: </strong> {movie.actor}</li>
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