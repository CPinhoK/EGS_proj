import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessageDelete';
import { useState } from 'react';


//var displayflag=false
//const data_recv=null

function DeleteWallet() {
  const [displayflag,setdisplayflag]= useState(false);
  const [displayalert,setdisplayalert]= useState(false);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/wallet');
  
  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }
  var onConfirm = () =>{
    console.log('Click Confirm')  
    if(walletid!=null && walletid.length>0){
        setfinal_url('http://localhost:8000/wallet/'+walletid);
      }else if(walletid==null||walletid.length === 0){
        setfinal_url('http://localhost:8000/wallet')
      }
      setdisplayflag(!displayflag)
      console.log(displayflag)
      console.log(final_url)
  }
  var onCancel = () =>{ console.log('Click Cancel'); setdisplayflag(false) }
  var onClick = () =>{
    console.log('Click')
    console.log(walletid);
    if( displayflag===false ) {
        setdisplayalert(!displayalert)
        window.confirm('Are you sure you wish to delete this wallet?') ? onConfirm("confirm") : onCancel("cancel")
    }else{
        setdisplayflag(false)
    }
  }
  return (
    <div className="mycontainer">
        <Header/>
        
        <div><h3>Input Wallet id</h3><h6>Warning: Wallet will be delted</h6> </div>
        <div><input className='input' type="text" onChange={getData_id} /> </div>

        <Button text='Delete Wallet'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={walletid}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default DeleteWallet;
//<Message url='http://localhost:8000/wallet'/>
