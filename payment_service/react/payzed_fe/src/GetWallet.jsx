import Header from './components/Header';
import './App.css';
import Button from './components/Button'
import Message from './components/MessageGET';
import { useState } from 'react';
import Fcookie from './components/Fcookie';
import { useCookies } from 'react-cookie';

//var displayflag=false
//const data_recv=null
const headers = {
  'Content-Type': 'application/json',
  'accept': 'application/json',
  'auth':'',
}

function GetWallet() {
  const [displayflag,setdisplayflag]= useState(false);
  const [walletid,setwalletid]= useState(null);
  const [final_url,setfinal_url]= useState('http://localhost:8000/wallet');
  const [cookies] = useCookies(['auth'])
  
  const getData_id = (val) =>{
    setwalletid(val.target.value);
    console.log(walletid);
  }

  var onClick = () =>{
    console.log('Click')
    console.log(walletid);
    if(walletid!=null && walletid.length>0){
      setfinal_url('http://localhost:8000/wallet/'+walletid);
    }else if(walletid==null||walletid.length === 0){
      setfinal_url('http://localhost:8000/wallet')
    }

    readcookiesandset();
    setdisplayflag(!displayflag)
    console.log(displayflag)
    console.log(final_url)
  }
  var readcookiesandset = () =>{
    headers.auth=cookies.auth
    console.log(headers)
  }
  return (
    <div className="mycontainer">
        <Header/>
        <Fcookie/>
        <h3>Input Wallet id</h3><h6> Leaving this field empy will return the info from all your wallets</h6>
        <div><input className='input' type="text" onChange={getData_id} /> </div>

        <Button text='Get Info'  onClick={onClick}/>
        <div>     
        {
            displayflag ? <Message url={final_url} inc_data={walletid} hin={headers}/> : <p></p>
        } 
        </div>

    </div>
  );
}

export default GetWallet;
//<Message url='http://localhost:8000/wallet'/>