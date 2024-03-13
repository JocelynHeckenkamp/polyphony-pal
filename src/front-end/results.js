import React, {useState,useEffect} from 'react';
import {OpenSheetMusicDisplay} from 'opensheetmusicdisplay';

function Results()
{
    const [data, setData] = useState();
    

  
//gets xml
    useEffect(()=>{
        fetch("/results") 
        .then(res => res.text())
        .then(data => {
          setData(data)
          
        }); 
        

        console.log(data);

    }, [])
    
//just displays raw xml string
    return(
    
       data
       
   
  );
  
    
}
export default Results;