import React,{useEffect} from 'react';
import { useNavigate } from "react-router-dom";

export default function Signup() {
    const navigate = useNavigate();
    var  Sign = () =>{
        window.confirm('You are being redirected to create an account')? OnConfirm("confirm") : OnCancel("cancel")
        }
      var OnConfirm = async () =>{
        useEffect(() => {
          console.log("Signup");
          //it would really help to send headers here 
          window.location.replace('http://127.0.0.1:8006/signup?redirectUrl='+window.location.host+'/params/');
          //window.location.replace('https://www.google.pt/search?q=HERE BE DRAGONS');
          //window.location.href='http://hugom.egs/Sign?redirectUrl='+window.location.host+'/params/';

        },[]); // eslint-disable-line react-hooks/exhaustive-deps
      
      };
    
      var OnCancel = async () =>{
        useEffect(() => {
          console.log("cancel")
          navigate("/", { replace: true })
        },[]);
      };
    
      return (
        <div>
            {Sign()}   
        </div>
      );
    }