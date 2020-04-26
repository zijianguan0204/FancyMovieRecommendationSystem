import React, {useEffect, useState} from 'react';
import '../bootstrap.css';
import '../App.css';
import axios from "axios";
import Slider from "react-slick";
import Slick_Card from './Slick_Card';

const config=require('../config/default');

function Slick() {
    const [suggestions,setSuggestions] = useState([]);

    useEffect(()=>{
        getSuggestions();
    },[]);

    const getSuggestions = ()=>{
        console.log('getSuggestions');
        axios.get(config.address+`/movieSuggestion?` +
            `&userId=${localStorage.getItem('access_token')==='true'?localStorage.getItem("user_id"):''}`)
            .then(function (response) {
                // handle success
                console.log(response);
                setSuggestions(response.data);
            })
            .catch(function (error) {
                // handle error
                console.log(error);
            })
    };

    const slickSettings = {
        dots: true,
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 3000,
        pauseOnHover: true,
        marginWidth:'10em',
    };


    return(
        <div style={{width:'70%', marginLeft:'15%'}}>
            <Slider {...slickSettings}>
                {suggestions.length>0? suggestions.map( data =>{
                    console.log('suggestion create');
                    return Slick_Card(data);
                }):<div>
                    {suggestions}
                </div>}
            </Slider>
        </div>
    )
}

export default Slick;