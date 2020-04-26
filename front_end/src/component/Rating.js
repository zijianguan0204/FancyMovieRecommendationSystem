import React, {useEffect, useState} from 'react';
import '../bootstrap.css';
import '../App.css';
import axios from "axios";
import Rating_Card from "./Rating_Card";

const config=require('../config/default');

function Rating() {
    const [ratings,setRating] = useState([]);

    useEffect(()=>{
        getRating();
        },[]
    );

    const getRating = ()=>{
        axios.get(config.address+`/moviesRating?` +
            `&userId=${localStorage.getItem('access_token')==='true'?localStorage.getItem("user_id"):''}`)
            .then(function (response) {
                // handle success
                console.log(response);
                setRating(response.data);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
    };

    return (
        ratings.length>0?<div id='searchMovie' className='row'>{
            ratings.map(rating =>{
                return Rating_Card(rating)
            })
        }</div>:<div/>
    );
}

export default Rating;