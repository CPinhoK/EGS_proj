import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePut';
import { useState } from 'react';
import Fcookie from './components/Fcookie';
import { useCookies } from 'react-cookie';
const headers = {
  'Content-Type': 'application/json',
  'accept': 'application/json',
  'auth':'',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': '*',
  'Access-Control-Request-Headers': '*',
}

function Transfer() {
  const [displayflag,setdisplayflag]= useState(false);
  const [walletid2,setwalletid2]= useState(null);
  const [walletid,setwalletid]= useState(null);
  const [cash,setcash]= useState(null);
  const [final_url,setfinal_url]= useState('//zppinho-papi.egs/wallet');
  const [cookies] = useCookies(['auth'])

  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }
  const getData_cash = (val) =>{
    console.log(val.target.value)
    setcash(parseFloat(val.target.value))
  }
  const getData_id2 = (val) =>{
    setwalletid2(val.target.value);
    console.log(walletid2);
  }
  var onClick = () =>{
    console.log('Click')
    console.log(walletid);
    readcookiesandset();
    if(walletid!=null && walletid.length>0){
      setfinal_url('//zppinho-papi.egs/transaction?from_wallet_id='+walletid+'&to_wallet_id='+walletid2+'&ammount='+cash);
    }
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
        <h4>Input Wallet id from where you want to take the cash</h4>
        <div><input className='input' type="text" onChange={getData_id} /> </div>
        <div><h4>Input Wallet id from where you want to put the cash</h4></div>
        <div><input className='input' type="text" onChange={getData_id2} /> </div>
        <h4>Input Cash to be transfered to the wallet</h4>
        <div><input className='input' type="text" onChange={getData_cash} /> </div>

        <Button text='Update Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} hin={headers} /> : <p></p>
        } 
        </div>

    </div>
  );
}

export default Transfer;
//<Message url='//zppinho-papi.egs/wallet'/>
