import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePOST_NR';
import { useState } from 'react';



const sapiCall = {
  username: null,
  password: null,
};

function Login() { 
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);

  const getData_user = (val) =>{
    apiCall.username=val.target.value
    setApicall(apiCall)
   
  }
  const getData_pass = (val) =>{
    apiCall.password=val.target.value
    setApicall(apiCall)
  }
  var onClick = () =>{
    console.log('Click')
    setdisplayflag(!displayflag)

  }

  return (
    <div className="mycontainer">
        <Header/>
        <h3>We will validate info at http://127.0.0.1:5000/</h3>
        <h3>Input username</h3>
        <div><input className='input' type="text" onChange={getData_user} /> </div>
        <h3>Input password</h3>
        <div><input className='input' type="text" onChange={getData_pass} /> </div>

        <Button text='Create Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url='https://virtserver.swaggerhub.com/hugo.moinheiro/auth/v1/login' inc_data={JSON.stringify(apiCall)}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default Login;
//<Message url='http://localhost:8000/wallet'/>
