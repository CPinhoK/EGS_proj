import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessagePut';
import { useState } from 'react';

const sapiCall = {
  cash_assoc:null,
  niff: null,
  wallet_desc: null,
};
//var displayflag=false
//const data_recv=null


function PutWallet() {
  const [displayflag,setdisplayflag]= useState(false);
  const [apiCall,setApicall]= useState(sapiCall);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/wallet');

  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }
  const getData_cash = (val) =>{
    console.log(val.target.value)
    apiCall.cash_assoc=parseFloat(val.target.value)
    setApicall(apiCall)
  }
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
    console.log(walletid);
    if(walletid!=null && walletid.length>0){
      setfinal_url('http://localhost:8000/wallet/'+walletid);
    }
    setdisplayflag(!displayflag)
    console.log(displayflag)
  }
  return (
    <div className="mycontainer">
        <Header/>
        <h4>Input Wallet id</h4>
        <div><input className='input' type="text" onChange={getData_id} /> </div>
        <div><h4>Input Niff </h4> <h6>(Leave value empty if you do not wish to change it)</h6> </div>
        <div><input className='input' type="text" onChange={getData_niff} /> </div>
        <div><h4>Input Wallet description </h4> <h6>(Leave value empty if you do not wish to change it)</h6> </div>
        <div><input className='input' type="text" onChange={getData_wallet_desc} /> </div>
        <h4>Input Cash to be transfered to this wallet</h4>
        <div><input className='input' type="text" onChange={getData_cash} /> </div>

        <Button text='Update Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={JSON.stringify(apiCall)}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default PutWallet;
//<Message url='http://localhost:8000/wallet'/>
