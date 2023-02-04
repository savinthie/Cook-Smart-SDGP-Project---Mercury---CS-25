import logo from './logo.svg';
import React,{useState} from 'react';
import './App.css';
import images from "./bro.svg";
import user from "./Customer.svg";
import lock from "./Lock.svg";
import {Login} from "./loginPage";


function App() {
  const[currentForm,setCurrentForm]=useState('Login');
  return (
    <div className="App">
      <img src= {images}alt="" id="logo"/>
      <img src= {user}alt="" id="user"/>
      <img src= {lock}alt=""id="lock" />
    <Login/>
       
    </div>
  );
}

export default App;
