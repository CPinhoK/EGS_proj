import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePut';
import { useState } from 'react';
import Fcookie from './components/Fcookie';
//var displayflag=false
//const data_recv=null


function Transfer() {
  const [displayflag,setdisplayflag]= useState(false);
  const [walletid2,setwalletid2]= useState(null);
  const [walletid,setwalletid]= useState(null);
  const [cash,setcash]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/wallet');

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
    if(walletid!=null && walletid.length>0){
      setfinal_url('http://localhost:8000/transaction?from_wallet_id='+walletid+'&to_wallet_id='+walletid2+'&ammount='+cash);
    }
    setdisplayflag(!displayflag)
    console.log(displayflag)
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
            displayflag ? <Message url={final_url} /> : <p></p>
        } 
        </div>

    </div>
  );
}

export default Transfer;
//<Message url='http://localhost:8000/wallet'/>
