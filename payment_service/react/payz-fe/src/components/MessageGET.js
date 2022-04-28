import React,{useState,useEffect} from 'react';
import axios from 'axios';
var JSONPrettyMon = require('react-json-pretty/dist/1337');
var JSONPretty = require('react-json-pretty');

export default function Message({url,inc_data}) {
  const[result,setResult] = useState(null);
  //const a = {url}
  //console.log(inc_data)

  const headers = {
    'Content-Type': 'application/json',
    'accept': 'application/json',
    'auth':'blabla@ua.pt toktok1',
  }
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
  const message = async () =>{
    try{
          let res = await axios.get(url,{
            headers: headers,
            data: inc_data
            });

	      console.log(res)
        let result = JSON.stringify(res.data);
        setResult(result);
        console.log(result)
    }catch(e){
        console.log(e)
        setResult(stringifyError(e.response, null, '\t'));
    }
  };

  useEffect(() => {
    message({url,inc_data}) 
  },[])  // eslint-disable-line react-hooks/exhaustive-deps

  return <div><JSONPretty data={result} theme={JSONPrettyMon}></JSONPretty></div>;
};


/* let res = await axios.get(url,{
    headers: {
      'auth': 'blabla@ua.pt toktok1'
    },
    data: inc_data
  }
); */

//return <div>{result}</div>;