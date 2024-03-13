import React, {useState,useEffect} from 'react';
import {OpenSheetMusicDisplay} from 'opensheetmusicdisplay';

function Results()
{
    const [data, setData] = useState();
    

  

    useEffect(()=>{
        fetch("/results") 
        .then(res => res.text())
        .then(data => {
          setData(data)
          
        }); 
        

        console.log(data);

    }, [])

    return(
    
       data
       
   
  );
  
    
}
export default Results;