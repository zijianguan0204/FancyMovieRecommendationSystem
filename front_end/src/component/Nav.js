import Navbar from "react-bootstrap/Navbar";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";
import React, {useEffect, useState} from "react";

function Nav() {
    const [login,setLogin] = useState(localStorage.getItem('access_token'));
    const [userId,setUserId] = useState(localStorage.getItem('user_id'));

    useEffect(()=>{
        console.log('type of id',typeof userId);
        if(!userId || userId.length<=0){
            localStorage.removeItem('user_id');
            localStorage.setItem('access_token', false);
            setLogin(false)
        }
    },[login]);

    if (login){
        return(
            <Navbar bg={'dark'} variant="dark">
                <Navbar.Brand href="/">Fancy Movie Recommender</Navbar.Brand>
                <Navbar.Toggle />
                <Navbar.Collapse className="justify-content-end">
                    <Form inline>
                        <Navbar.Text className="mr-sm-2">
                            Signed in as: <a>{localStorage.getItem('user_id')}</a>
                        </Navbar.Text>
                        <Button type="submit" onClick={event => {
                            localStorage.removeItem('user_id');
                            localStorage.setItem('access_token', false);
                            setLogin(false);
                            window.location.reload();
                        }} size={'sm'}>Sign out</Button>
                    </Form>
                </Navbar.Collapse>
            </Navbar>
        )
    }
    return(
        <Navbar bg={'dark'} variant="dark">
            <Navbar.Brand href="/">Fancy Movie Recommender</Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
                <Form inline>
                    <FormControl type="text" placeholder="User Id" className=" mr-sm-2" size={"lg"}
                        onChange={(event => {
                            setUserId(event.target.value);
                            })
                        }
                    />
                    <button type="submit" onClick={event => {
                        localStorage.setItem('user_id',userId);
                        localStorage.setItem('access_token', true);
                        setLogin(true);
                        window.location.reload();
                    }}  className="btn btn-secondary" >Sign in</button>
                </Form>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default Nav;