import {Link} from "react-router-dom";
import React from "react";
import Rating from '@material-ui/lab/Rating';
import Box from '@material-ui/core/Box';

function Rating_Card(movie) {
    return(
        <div className="col-md-3">
            <div className='well text-center'>
                <img src={movie.poster} alt={movie.title}/>
                <h5>{movie.title}</h5>
                <Box component="fieldset" mb={3} borderColor="transparent" >
                    <Rating
                        name="simple-controlled"
                        size="samll"
                        value={Math.max(movie.rating,0)}
                        readOnly
                    />
                </Box>
                <Link to={`/movie/${movie.id}`} className = 'btn btn-primary' style={{marginTop:'-2em'}}>View Detail</Link>
            </div>
        </div>
    );
}

export default Rating_Card;