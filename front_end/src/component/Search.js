import React , {useState, useEffect}from 'react';
import '../bootstrap.css';
import '../App.css';
import axios from "axios";

function Search() {
    const [search,setSearch] = useState('');
    const [isLoad,setIsLoad] = useState(true);
    const [error,setError] = useState(null);
    const [movie,setMovie] = useState([]);

    useEffect(()=>{

    });

    const searchMovie = ()=>{
        axios.get(`http://localhost:5000/movieSearch?` +
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

    return(
        <div className="container">
            <div className="jumbotron">
                <h3 className="text-center">Search For Any Movie</h3>
                <form id="searchForm">
                    <input type="text" className="form-control" id="searchText" placeholder="Search Movies..."
                    onChange={(event => {
                        console.log(event.target.value,search);
                        setSearch(event.target.value);
                    })}
                    />
                </form>
            </div>
        </div>
    )
}

export default Search;