import React, { useState } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { TextField,  Paper, Grid, CircularProgress, Typography, Button, Select, MenuItem, FormControl, InputLabel, OutlinedInput } from '@mui/material';
import Header from './components/polypalHeader';
import Keydropdown from './components/keysigdropdown';
import css from "./components/frontEnd.module.css"

function Generation(){
    //ddvalue = key
    //text value = roman numerals
    const [ddValue, setDD] = useState("");
    const [textVal, setTextVal] = useState("");
    //false = spinner not showing
    const [spinner, setSpinner] = useState(false);
    const [generating, setGen] = useState(false);
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
            setGen(true)
        }
        setMusicXML(xmls);

        const interval = setInterval(async () => {
            const res = await fetch(`/RomanScore/${id}/XML`, {
            method: 'GET'
            });
            const data = await res.json();
            const xmls = data.xmls;
            if ( xmls.length > 0 || data.finished) {
                setSpinner(false)
                setGen(true)
            }
            setMusicXML(xmls);

            if (data.finished) {
            clearInterval(interval); // Stop polling if finished
            setGen(false)
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

const circleOfFifths = "C,G,D,A,E,B,C-,F#,G-,C#,D-,A-,E-,B-,F,a,e,b,f#,c#,g#,e-,d#,b-,f,c,g,d".split(',');const title ="Generate Music"
const subtitle ="Input chords/roman numerals and key signature"
const thirdtitle ="Please enter a comma separated list ex) I,ii,V7,I"
const arr = {upload_title: title, upload_subtitle: subtitle, upload_thirdtitle: thirdtitle}

const render_content = () =>
{   
    if(spinner){ //if waiting on data, show spinner
        return(<div><CircularProgress/> <p>Waiting to generate data</p></div>);
    }
    else{
        if(musicXML){//if data is recieved, render it
            return <>
                {generating ? (<div><CircularProgress/> <p>Generating Data</p></div>) : (null)}
                
                
                {musicXML.map(xml => 
                <Grid pb={2} maxWidth={"50vh"}>
                <Paper className={css.music_paper} >
                <SheetMusicComponent musicXml={xml.xml} key={xml.id} />
                </Paper>
                </Grid>)}
                
                </>;
        }
        else{//wait for user input
            
            return(
                <div>
                <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}} className={css.flex_container} >
                    <Grid item align="center">
                    <Paper className={css.upload_paper} elevation={3}>
                        {Object.keys(arr).map(key => <Typography className={css[key]}>{arr[key]}</Typography>)}
                        {console.log(Object.keys(arr))}
                        
                        <TextField id="outlined-basic" label="Roman Numerals" variant="outlined" sx={{width: 200}} value={textVal} onChange={handleTextChange}/>
                        
                        <FormControl variant="outlined" sx={{width:175}}>
                        <InputLabel id="Key">Key Signature</InputLabel>
                        <Select value={ddValue} onChange={handleDDchange} input={<OutlinedInput label="Key Signature" />}>
                            {circleOfFifths.map(key => <MenuItem key={key} value={key} >{key}</MenuItem>)}
                        </Select>
                        </FormControl> 
                        <Button className={css.btnLG} onClick={upload}>Upload</Button>
                    </Paper>  
                </Grid>
            </Grid>
            <div className={css.upload_background}></div>
            </div>
            );
        }
    }

}
    return(
        <div >
            
            <Header />
            {render_content()}
            
        </div>
    );
}
export default Generation;


