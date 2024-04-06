import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Container, Select,MenuItem, Button, Grid } from '@mui/material';
import Header from './components/polypalHeader';

function Generation(){
    //ddvalue being sent to backend
    const [ddValue, setDD] = useState([]);
    const [data, setData] = useState();
    const [musicXML, setMusicXML] = useState('');

const handleDDchange = (e) => {
    setDD(e.target.value);
    console.log(ddValue)
}
//upload to api music_generation function
const upload = () => {
    fetch("/musicGeneration",
      {
        method: "POST",
        body: ddValue,
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
            
            <Select value={ddValue} onChange={handleDDchange} multiple>
                <MenuItem value={"I"}>I</MenuItem>
                <MenuItem value={"II"}>II</MenuItem>
                <MenuItem value={"III"}>III</MenuItem>
                <MenuItem value={"IV"}>IV</MenuItem>
                <MenuItem value={"V"}>V</MenuItem>
                <MenuItem value={"VI"}>VI</MenuItem>
                <MenuItem value={"VII"}>VII</MenuItem>
            </Select>
            <Button onClick={upload}>Hello world</Button>
        </Grid>
    }

    </div>
    );
}
export default Generation;