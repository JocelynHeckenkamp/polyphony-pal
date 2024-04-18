import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { TextField, Select,MenuItem, Button, Grid, CircularProgress } from '@mui/material';
import Header from './components/polypalHeader';

function Generation(){
    //ddvalue = key
    //text value = roman numerals
    const [ddValue, setDD] = useState("");
    const [textVal, setTextVal] = useState("");
    const [data, setData] = useState();
    //false = spinner not showing
    const [spinner, setSpinner] = useState(false);
    const [musicXML, setMusicXML] = useState('');

const handleTextChange = (e) => {
    setTextVal(e.target.value);
    console.log(textVal)
}

 const handleDDchange = (e) => {
    setDD(e.target.value);
    console.log(textVal)
    
}
//upload to api music_generation function
const upload = async () => {
    
    const values = [ ddValue, textVal ]
    try {
        setSpinner(true)
        let res = await fetch("/musicGeneration",
            {
                method: "POST",
                body: JSON.stringify({values}) ,
                headers: {
                    "Content-Type": "application/json"
                }
            })
        let data = await res.json()
        let id = data.id 
        console.log(data)

        res = await fetch(`/RomanScore/${id}/XML`, {
            method: 'GET'
        });
        data = await res.json();
        const xmls = data.xmls;
        if (xmls.length > 0 || data.finished) {
            setSpinner(false)
        }
        setMusicXML(xmls);

        const interval = setInterval(async () => {
            const res = await fetch(`/RomanScore/${id}/XML`, {
            method: 'GET'
            });
            const data = await res.json();
            const xmls = data.xmls;
            if (xmls.length > 0 || data.finished) {
                setSpinner(false)
            }
            setMusicXML(xmls);

            if (data.finished) {
            clearInterval(interval); // Stop polling if finished
            }
        }, 10000); // Poll every 10 seconds (10000 milliseconds)

        // setMusicXML(data);
        // setSpinner(false);
    }
    catch(error) {
        console.error("Error during the upload process:", error) 
    }
  }
//once music is set, render
//drop down to be removed!

const circleOfFifths = "C,G,D,A,E,B,C-,F#,G-,C#,D-,A-,E-,B-,F,a,e,b,f#,c#,g#,e-,d#,b-,f,c,g,d".split(',');

const render_content = () =>
{   
    if(spinner){ //if waiting on data, show spinner
        return(<CircularProgress/>);
    }
    else{
        if(musicXML){//if data is recieved, render it
            return <>{musicXML.map(xml => <SheetMusicComponent musicXml={xml.xml} key={xml.id} />)}</>;
        }
        else{//wait for user input
            return(
                <Grid>
                <TextField id="outlined-basic" label="Roman Numerals" variant="outlined" value={textVal} onChange={handleTextChange}/>
                <Select value={ddValue} onChange={handleDDchange}>
                    {circleOfFifths.map(key => <MenuItem key={key} value={key}>{key}</MenuItem>)}
                </Select> 
                
                <Button onClick={upload}>Upload</Button>
            </Grid>
            );
        }
    }

}
    return(
        <div>
            <Header/>
            {render_content()}
        </div>
    );
}
export default Generation;


