import React,{useEffect} from 'react';

import { useNavigate } from "react-router-dom";


export default function Redirect() {
  const navigate = useNavigate();
  //useEffect(() => {console.log("Read Cookie")},[]) 

  var  RedirectGO = () =>{

    true ? OnConfirm("confirm") : OnCancel("cancel")
    
  }
  var OnConfirm = async () =>{
    var url = window.location.href;
    console.log(url);
    const rurl=url.split('?url=')[1];
    console.log(rurl);

    //const[result,setResult] = useState(null);
    useEffect(() => {
      console.log("login");

      window.location.replace('https://hugom.egs/login?redirectUrl='+rurl);

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
        {RedirectGO()}   
    </div>
  );
}
