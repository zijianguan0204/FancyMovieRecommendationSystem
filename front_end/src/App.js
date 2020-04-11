import React from 'react';
import './bootstrap.css';
import './App.css';
// import Greet from "./component/Greet";
// import Welcome from "./component/Welcome";
// import Counter from "./component/Count";
import Login from "./component/Login"
import Movie from "./component/Movie"
import Search from "./component/Search"
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';

function App() {
    localStorage.setItem('access_token', true);
    localStorage.setItem('user_id', 'test1');
    if (!localStorage.getItem('access_token')){
        return (
            <Login/>
        );
    }
  return [
      <Nav/>
      ,
      <Router>
          <div className="App">
              <Switch>
                  <Route exact path = '/' component={Search}/>
                  <Route path = '/movie/:id' component={Movie}/>
              </Switch>
              {/*<Search/>*/}
            {/*<Counter/>*/}
            {/*<Greet name = 'LSC'/>*/}
            {/*<Welcome/>*/}
          </div>
      </Router>
  ];
}

function Nav() {
    return(
        <nav className="navbar navbar-default">
            <div className="container">
                <div className="navbar-header">
                    <a className="navbar-brand" href="/">Fancy Movie Recommendation</a>
                </div>
            </div>
        </nav>
    );
}

export default App;
