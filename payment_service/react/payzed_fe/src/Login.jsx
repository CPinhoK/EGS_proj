import React,{useEffect} from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from "react-router-dom";


export default function Login() {
  // eslint-disable-next-line
  const [cookies, setCookie] = useCookies(['auth'])  
  const navigate = useNavigate();

    function  SetCoo(){
      console.log(window.location.pathname)
      console.log( window.location.href)
      const queryString = window.location.href.replace('/params/','');
      console.log(queryString);
      const urlParams = new URLSearchParams(queryString);
      const user = urlParams.get('user')
      console.log(user);
      

      var url = window.location.href;
      var token =url.substring(url.lastIndexOf('/')+1);
      token=token.split('=')[1].split('&')[0];
      console.log(token);

      let expires = new Date();
      let h = 1 // 1 hour 
      expires.setTime(expires.getTime() + (h*60*60*1000) );
      let authi = user+" "+token;
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
