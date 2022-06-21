import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessageDelete';
import { useState } from 'react';
import Fcookie from './components/Fcookie';
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

function DeleteWallet() {
  const [displayflag,setdisplayflag]= useState(false);
  const [displayalert,setdisplayalert]= useState(false);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('//zppinho-papi.egs/wallet');
  const [cookies] = useCookies(['auth'])
  
  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }
  var onConfirm = () =>{
    console.log('Click Confirm')  
    if(walletid!=null && walletid.length>0){
        setfinal_url('//zppinho-papi.egs/wallet/'+walletid);
      }else if(walletid==null||walletid.length === 0){
        setfinal_url('//zppinho-papi.egs/wallet')
      }
      setdisplayflag(!displayflag)
      console.log(displayflag)
      console.log(final_url)
  }
  var onCancel = () =>{ console.log('Click Cancel'); setdisplayflag(false) }
  var onClick = () =>{
    readcookiesandset();
    console.log('Click')
    console.log(walletid);
    if( displayflag===false ) {
        setdisplayalert(!displayalert)
        window.confirm('Are you sure you wish to delete this wallet?') ? onConfirm("confirm") : onCancel("cancel")
    }else{
        setdisplayflag(false)
    }
  }
  var readcookiesandset = () =>{
    headers.auth=cookies.auth
    console.log(headers)
  }
  return (
    <div className="mycontainer">
        <Header/>
        <Fcookie/>
        
        <div><h3>Input Wallet id</h3><h6>Warning: Wallet will be delted</h6> </div>
        <div><input className='input' type="text" onChange={getData_id} /> </div>

        <Button text='Delete Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={walletid} hin={headers}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default DeleteWallet;
//<Message url='//zppinho-papi.egs/wallet'/>
