import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePost';
import { useState } from 'react';

const sapiCall = {
  niff: null,
  wallet_desc: null,
};
//var displayflag=false
//const data_recv=null


function App() {
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);
  
  const getData_niff = (val) =>{
    console.log(val.target.value)
    apiCall.niff=parseInt(val.target.value)
    setApicall(apiCall)
  }
  const getData_wallet_desc = (val) =>{
    console.log(val.target.value)
    apiCall.wallet_desc=val.target.value
    setApicall(apiCall)
  }
  var onClick = () =>{
    console.log('Click')
    console.log(apiCall)
    console.log(JSON.stringify(apiCall))
    setdisplayflag(!displayflag)
    console.log(displayflag)
  }
  return (
    <div className="mycontainer">
        <Header/>
        
        <h3>Input Niff</h3>
        <div><input className='input' type="text" onChange={getData_niff} /> </div>
        <h3>Input Wallet description</h3>
        <div><input className='input' type="text" onChange={getData_wallet_desc} /> </div>

        <Button text='Create Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url='http://localhost:8000/wallet' inc_data={JSON.stringify(apiCall)}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default App;
//<Message url='http://localhost:8000/wallet'/>
