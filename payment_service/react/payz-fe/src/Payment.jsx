import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePost';
import { useState } from 'react';
import { useCookies } from 'react-cookie';

//var displayflag=false
//const data_recv=null
const headers = {
  'Content-Type': 'application/json',
  'accept': 'application/json',
  'auth':'',
}

const sapiCall = {
  incoming_paymentid:"hey",
  totaltopay: 0.0,
  metodo_de_pagamento: null,
  source: null,
  payment_desc: null,
  timestamp_recv: null,
};
//var displayflag=false
//const data_recv=null
function Payment() {
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/payment?wallet_id=');
  const [cookies] = useCookies(['auth'])
  setApicall(sapiCall)
  
  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }
  var onClick = () =>{
    console.log('Click')
    console.log(apiCall)
    readcookiesandset();
    setfinal_url(final_url+walletid)
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
        <h5>Source:{sapiCall.source} </h5>
        <h5>Total to pay:{sapiCall.totaltopay} </h5>
        <h5>Payment description:{sapiCall.payment_desc} </h5>
        <h5>Choose wallet to make the payment</h5>
        <div><input className='input' type="text" onChange={getData_id} /> </div>

        <Button text='Make payment'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={JSON.stringify(apiCall)} hin={headers}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default Payment;
//<Message url='http://localhost:8000/wallet'/>
