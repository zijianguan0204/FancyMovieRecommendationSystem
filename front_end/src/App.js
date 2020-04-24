import React from 'react';
import './bootstrap.css';
import './App.css';
import Movie from "./component/Movie"
import Search from "./component/Search"
import Nav from "./component/Nav"
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

function App() {
    // localStorage.setItem('access_token', false);
    // localStorage.setItem('user_id', 'test1');
    // if (!localStorage.getItem('access_token')){
    //     return (
    //         <Login/>
    //     );
    // }
  return [
      <Nav/>
      ,
      <Router>
          <div className="App">
              <Switch>
                  <Route exact path = '/' component={Search}/>
                  <Route path = '/movie/:id' component={Movie}/>
              </Switch>
          </div>
      </Router>
  ];
}



export default App;
