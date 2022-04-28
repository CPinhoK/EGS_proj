import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessageGET';
import { useState } from 'react';
import Fcookie from './components/Fcookie';

//var displayflag=false
//const data_recv=null

function GetPaymentHist() {
  const [displayflag,setdisplayflag]= useState(false);
  const [paymentid,setpayment]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/payment');
  
  const getData_id = (val) =>{
    setpayment(val.target.value);
    console.log(paymentid);
  }

  var onClick = () =>{
    console.log('Click')
    console.log(paymentid);
    if(paymentid!=null && paymentid.length>0){
      setfinal_url('http://localhost:8000/payment/'+paymentid);
    }else if(paymentid==null||paymentid.length === 0){
      setfinal_url('http://localhost:8000/payment')
    }
    setdisplayflag(!displayflag)
    console.log(displayflag)
    console.log(final_url)
  }
  return (
    <div className="mycontainer">
        <Header/>
        <Fcookie/>
        <h3>Input Payment id</h3><h6> Leaving this field empy will return the info from all your Payments from all your wallets</h6>
        <div><input className='input' type="text" onChange={getData_id} /> </div>

        <Button text='Get Info'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={paymentid}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default GetPaymentHist;
//<Message url='http://localhost:8000/wallet'/>
