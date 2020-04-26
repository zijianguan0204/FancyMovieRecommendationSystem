import React , {useState, useEffect}from 'react';
import '../bootstrap.css';
import '../App.css';
import axios from "axios";
import Slick from "./Slick";
import Search_Card from './Search_Card';
import Rating from "./Rating";

const config=require('../config/default');

function Search() {
    const [search,setSearch] = useState('');
    const [isLoad,setIsLoad] = useState(true);
    const [error,setError] = useState(null);
    const [movie,setMovie] = useState([]);

    useEffect(()=>{
        console.log(movie);
    },[movie]);


    const searchMovie = ()=>{
        axios.get(config.address+`/movieSearch?` +
            `search=${search}`)
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

    const searchMovieList = ()=>{
        let output = [];
        movie.forEach(m =>{
            output.push(Search_Card(m));
        });
        console.log(output);
        return output;
    };

    return[
        <div className="container">
            <div className="jumbotron">
                <h3 className="text-center">Search For Any Movie</h3>
                <form className="form-inline" id="searchForm" >
                    <input type="text" className="form-control" id="searchText" placeholder="Search Movies... Try: HP"
                           onChange={(event => {
                               setSearch(event.target.value);
                           })}
                           onKeyDown={(event => {
                               if (event.key === 'Enter'){
                                   event.preventDefault();
                                   console.log('start search',search);
                                   searchMovie();
                               }
                           })}
                           style={{width:'50em',marginLeft:'10%'}}
                    />
                    <button className="btn btn-primary" onClick={event => {
                        event.preventDefault();
                        searchMovie();
                    }}>Search</button>
                </form>
            </div>
        </div>,
        movie.length>0?<div id='searchMovie' className='row'>{searchMovieList()}</div>:<div/>,
        <div style={{marginBottom:"30px"}}>
            <h2 style={{margin:"20px"}}>You May Like</h2>
            <Slick/>
        </div>,
        <div style={{marginBottom:"30px"}}>
            <h2 style={{margin:"20px"}}>Your Rating</h2>
            <Rating/>
        </div>
    ];
}

export default Search;