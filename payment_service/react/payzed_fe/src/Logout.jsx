import React,{useEffect,useState} from 'react';
import { useNavigate } from "react-router-dom";
import { useCookies } from 'react-cookie';
import axios from 'axios';
import Header from './components/Header';
const url = 'http://hugom.egs/logout'
//const url = 'http://127.0.0.1:8006/logout'
const headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Request-Headers': '*',
}

export default function Logout() {
    const navigate = useNavigate();
    const [cookies] = useCookies(['auth'])// eslint-disable-next-line
    const[result,setResult] = useState(null);
    var  Logo = () =>{
        window.confirm('You will be logged out')? OnConfirm("confirm") : OnCancel("cancel")
        }

      var OnConfirm = async () =>{
        useEffect(() => {
          },[]);
        try{
            let user=cookies.auth
            user=user.split(' ')[0]
            let inc_data={'user':user};
            let res = await axios.post(url, inc_data, {
                headers: headers
              })
              console.log(res)
            console.log(res.status);  
            let result = JSON.stringify(res.data);
            setResult(result);
            console.log(result)
            if(result===''||result===undefined||result===""){
                console.log("aaaaaaaaaa")
                window.location.replace(window.location.host);
            }
        }catch(e){
            console.log(e)
            
        }
        navigate("/", { replace: true })
      };
    
      var OnCancel = async () =>{
        useEffect(() => {
          console.log("cancel")
          navigate("/", { replace: true })
        },[]);
      };
    
      return (
        <div>
            {Logo()}   
            <div className="mycontainer">
            <Header/>
            <h1>LOGGED OUT</h1>
            </div>
        </div>
      );
    }