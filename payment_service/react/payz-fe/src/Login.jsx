import React,{useEffect} from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from "react-router-dom";


export default function Login() {
  // eslint-disable-next-line
  const [cookies, setCookie] = useCookies(['auth'])  
  const navigate = useNavigate();

    function  SetCoo(){
      console.log( window.location.href)
      let x = window.location.pathname
      console.log(x)
      x=x.split("_")
      console.log(x[1])
      let token = x[1]
      let user = x[2]

      let expires = new Date();
      let h = 1 // 1 hour 
      expires.setTime(expires.getTime() + (h*60*60*1000) );
      let authi = user+" "+ token;
      console.log(authi)
      setCookie('auth', authi, { path: '/',  expires, sameSite: "none",secure: true});

      useEffect(() => {
        navigate("/", { replace: true })
      },[]);

    }

  return (
    <div>
        {SetCoo()}   
    </div>
  );
}
