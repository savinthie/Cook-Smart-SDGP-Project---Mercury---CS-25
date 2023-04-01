//to capture user entered values
import React,{ useState } from "react";



//how the form is structured
export const  Login =()=>{
    const [email,setEmail]=useState('');//initialise the value to empty & store the value of the email
    const [password,setPassword]=useState('');//initialise the value to empty & store the values of the password
    
    const handleSubmit=(event)=>{
        event.preventDefault();//to avoid losing the state once the page get reloaded
        console.log(email);
        console.log(password)
    }
    
    return(
        <div classsName="container">
            
           
        
            <h1>LOGIN</h1>
            <form  className="loginForm" onSubmit={handleSubmit}>
                <label  for = "email"> Email: </label>
                <input type="email" onChange={(event)=> setEmail(event.target.value)} id="email"value={email}/>
                <label  for = "password"> Password: </label>
                <input type="password" onChange={(event)=> setPassword(event.target.value)}id="password"value={password}/>
                <br /><br />
                <div className="buttonContainer">
                <button type="submit">LOGIN</button>
                <p>Need an account? <u>SIGN UP</u></p>
                </div>
            </form>
       </div>
    )
}