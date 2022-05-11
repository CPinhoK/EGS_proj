import React,{useState,useEffect} from 'react';
import axios from 'axios';
import { useCookies } from 'react-cookie';


export default function Message({url,inc_data,hin}) {
  // eslint-disable-next-line
  const [cookies, setCookie] = useCookies(['auth'])  
  const[result,setResult] = useState(0);
  let user=JSON.parse(inc_data).username;

  //const a = {url}
  //console.log(user)

  const headers = hin
  var stringifyError = function(err, filter, space) {
    var plainObject = {};
    Object.getOwnPropertyNames(err).forEach(function(key) {
      if(key!=='data' && key!=='status' && key!=='statusText'){
        return JSON.stringify(plainObject, filter, space);
      }
      plainObject[key] = err[key];
    });
    return JSON.stringify(plainObject, filter, space);
  };
  
  const Tmessage = async () =>{
    try{
        let res = await axios.post(url, inc_data, {
            headers: headers
          })
	    //console.log(res)
        let result = res.data;
        console.log(result.token);
        let tok= await result.token
        setResult(tok);
        //console.log(result.token)
    }catch(e){
        console.log(e)
        setResult(stringifyError(e.response, null, '\t'));
    }


    let expires = new Date();
    let h = 1 // 1 hour 
    expires.setTime(expires.getTime() + (h*60*60*1000) );
    let authi = await user+" "+ result;
    console.log(authi)
    setCookie('auth', authi, { path: '/',  expires, sameSite: "none",secure: true});

  
  };


  useEffect(() => {
    Tmessage({url,inc_data,hin})
  },[result])  // eslint-disable-line react-hooks/exhaustive-deps
  return <div>Logged IN</div>;
  //return <div>{result}</div>;
};


/* let res = await axios.get(url,{
    headers: {
      'auth': 'blabla@ua.pt toktok1'
    },
    data: inc_data
  }
); */