import {Link} from "react-router-dom";
import React from "react";

function Slick_Card(movie) {
    return(
            <div>
                <img src={'https://image.tmdb.org/t/p/original'+movie.poster} alt={movie.title} style={{height:450,width:320}}/>
                <h5>{movie.title}</h5>
                <Link to={`/movie/${movie.id}`} className = 'btn btn-primary'>View Detail</Link>
            </div>
    );
}

export default Slick_Card;