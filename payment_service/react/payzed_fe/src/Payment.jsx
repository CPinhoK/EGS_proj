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
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Request-Headers': '*',
}

const sapiCall = {
  incoming_paymentid:"hey",
  totaltopay: 1.3,
  metodo_de_pagamento: null,
  source: null,
  payment_desc: null,
  timestamp_recv: null,
};



//var displayflag=false
//const data_recv=null
function Payment() {
  console.log("b")
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('//zppinho-papi.egs/payment?wallet_id=');
  const [cookies] = useCookies(['auth'])
  
  
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
    setApicall(sapiCall)
  }
  var readcookiesandset = () =>{
    headers.auth=cookies.auth
    console.log(headers)
  }
  console.log("c")
  
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
//<Message url='//zppinho-papi.egs/wallet'/>
