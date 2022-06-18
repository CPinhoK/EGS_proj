import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePost';
import { useState } from 'react';

import Fcookie from './components/Fcookie';
import { useCookies } from 'react-cookie';


const sapiCall = {
  niff: null,
  wallet_desc: null,
};
//var displayflag=false
//const data_recv=null
const headers = {
  'Content-Type': 'application/json',
  'accept': 'application/json',
  'auth':'',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Request-Headers': '*',
}

function CreateWallet() { //CREATE WALLET
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);
  const [cookies] = useCookies(['auth'])

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
    readcookiesandset()
    setdisplayflag(!displayflag)
    console.log(displayflag)

  }
  var readcookiesandset = () =>{
    headers.auth=cookies.auth
    console.log(headers)
  }
  return (
    <div className="mycontainer">
        <Header/>
        <Fcookie/>
        <h3>Input Niff</h3>
        <div><input className='input' type="text" onChange={getData_niff} /> </div>
        <h3>Input Wallet description</h3>
        <div><input className='input' type="text" onChange={getData_wallet_desc} /> </div>

        <Button text='Create Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url='//zppinho-papi.egs/wallet' inc_data={JSON.stringify(apiCall)} hin={headers}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default CreateWallet;
//<Message url='//zppinho-papi.egs/wallet'/>
