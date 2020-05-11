import {Link} from "react-router-dom";
import React from "react";
import image_not_found from '../not_found.png'

function Slick_Card(movie) {
    return(
            <div>
                <img src={'https://image.tmdb.org/t/p/original'+movie.poster} alt={movie.title} style={{height:450,width:320}}
                     onError={(e) => {
                         e.target.src = image_not_found //replacement image imported above
                     }}/>
                <h5>{movie.title}</h5>
                <p>{movie.tag}</p>
                <Link to={`/movie/${movie.id}`} className = 'btn btn-primary'>View Detail</Link>
            </div>
    );
}

export default Slick_Card;