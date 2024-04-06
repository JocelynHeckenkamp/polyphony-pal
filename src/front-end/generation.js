import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { TextField, Select,MenuItem, Button, Grid } from '@mui/material';
import Header from './components/polypalHeader';

function Generation(){
    //ddvalue being sent to backend
    //const [ddValue, setDD] = useState([]);
    const [textVal, setTextVal] = useState("");
    const [data, setData] = useState();
    const [musicXML, setMusicXML] = useState('');

const handleTextChange = (e) => {
    setTextVal(e.target.value);
    console.log(textVal)
}
//upload to api music_generation function
const upload = () => {
    fetch("/musicGeneration",
      {
        method: "POST",
        body: textVal,
      })
      .then(response => response.text())
      .then(data => {
        setMusicXML(data);
        
        //set loading bar false AFTER data has been set
      })
      .catch(error => console.error("Error during the upload process:", error));
  }
//once music is set, render

    return(
    <div>
    <Header/>
    {musicXML ? ( <SheetMusicComponent musicXml={musicXML} />) : 
        <Grid>
            <TextField id="outlined-basic" label="Roman Numerals" variant="outlined" value={textVal} onChange={handleTextChange}/>
            
            <Button onClick={upload}>Hello world</Button>
        </Grid>
    }

    </div>
    );
}
export default Generation;


/* <Select value={ddValue} onChange={handleDDchange} multiple>
                <MenuItem value={"I"}>I</MenuItem>
                <MenuItem value={"II"}>II</MenuItem>
                <MenuItem value={"III"}>III</MenuItem>
                <MenuItem value={"IV"}>IV</MenuItem>
                <MenuItem value={"V"}>V</MenuItem>
                <MenuItem value={"VI"}>VI</MenuItem>
                <MenuItem value={"VII"}>VII</MenuItem>
            </Select> */