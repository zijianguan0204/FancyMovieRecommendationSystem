import {Link} from "react-router-dom";
import React from "react";

function Search_Card(movie) {
    return(
        <div className="col-md-3">
            <div className='well text-center'>
                <img src={'https://image.tmdb.org/t/p/original'+movie.poster} alt={movie.title}/>
                <h5>{movie.title}</h5>
                <Link to={`/movie/${movie.id}`} className = 'btn btn-primary'>View Detail</Link>
            </div>
        </div>
    );
}

export default Search_Card;