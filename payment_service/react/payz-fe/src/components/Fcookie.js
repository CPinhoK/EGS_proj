import React,{useState,useEffect} from 'react';
import { useCookies } from 'react-cookie';
import axios from 'axios';
import { useNavigate } from "react-router-dom";

export default function F_cookie() {
  const [result,setResult] = useState(null);
  const [cookies, setCookie] = useCookies(['auth'])
  const navigate = useNavigate();
  setResult(null);
  useEffect(() => {console.log("Read Cookie")},[]) 

  var  Readcookie = () =>{
    console.log(cookies.auth);
    
    let expires = new Date();
    let h = 1 // 1 hour 
    expires.setTime(expires.getTime() + (h*60*60*1000) );
    console.log(expires)
    setCookie('auth', "blabla@ua.pt asdsdaw", { path: '/',  expires, sameSite: "none",secure: true}); /* Manual mode */

    if(cookies.auth===null||cookies===undefined){
      window.confirm('You are not Authenticated press Ok to authenticate')? OnConfirm("confirm") : OnCancel("cancel")
    }
  }
  var OnConfirm = async () =>{
    try{
        //window.open('https://www.google.com', '_blank');
        let res = await axios.get('http://localhost:3000/auther');
        console.log(res)
        let result = JSON.stringify(res.data);
        setResult(result);
        console.log(result)
    }catch(e){
        console.log(e)
        setResult(e.response, null, '\t');
    }
    if(result){
      //do nothing
    }
    let expires = new Date();
    let h = 1 // 1 hour 
    expires.setTime(expires.getTime() + (h*60*60*1000) );
    //setCookie('auth', result, { path: '/',  expires, sameSite: "none",secure: true});
  
  };

  var OnCancel = async () =>{
    useEffect(() => {
      console.log("cancel")
      navigate("/", { replace: true })
    },[]);
  };

  return (
    <div>
        {Readcookie()}   
    </div>
  );
}

//<Message url='http://localhost:8000/wallet'/>
