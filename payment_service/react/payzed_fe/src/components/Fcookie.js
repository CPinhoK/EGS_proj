import React,{useEffect} from 'react';
import { useCookies } from 'react-cookie';
import { useNavigate } from "react-router-dom";


export default function F_cookie() {
  const [cookies] = useCookies(['auth'])
  const navigate = useNavigate();
  //useEffect(() => {console.log("Read Cookie")},[]) 

  var  Readcookie = () =>{
    console.log(cookies.auth);

    if(cookies.auth===null||cookies.auth===undefined){
      window.confirm('You are not Authenticated press Ok to authenticate')? OnConfirm("confirm") : OnCancel("cancel")
    }
  }
  var OnConfirm = async () =>{
    //const[result,setResult] = useState(null);
    useEffect(() => {
      console.log("login");
      //it would really help to send headers here 
      window.location.replace('http://127.0.0.1:8006/login?redirectUrl=https://'+window.location.host+'/params/');
      //window.location.href='http://hugom.egs/login?redirectUrl='+window.location.host+'/params/';
      // const message = async () =>{
      //   try{
      //       let res = await axios.get('http://127.0.0.1:8006/login');
      //       console.log(res)
      //       let result = JSON.stringify(res.data);
      //       setResult(result);
      //       console.log(result)
      //   }catch(e){
      //       console.log(e)
      //   }
      //   };
      //   message() 
        //console.log(result)
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
        {Readcookie()}   
    </div>
  );
}

//<Message url='//zppinho-papi.egs/wallet'/>

/*
  var OnConfirm = async () =>{
    try{
        //window.open('https://www.google.com', '_blank');
        let res = await axios.get('//papi:3000/auther');
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
*/