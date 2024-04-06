import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { TextField, Select,MenuItem, Button, Grid } from '@mui/material';
import Header from './components/polypalHeader';

function Generation(){
    //ddvalue = key
    //text value = roman numerals
    const [ddValue, setDD] = useState([]);
    const [textVal, setTextVal] = useState("");
    const [data, setData] = useState();
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
const upload = () => {

    const values = [ ddValue, textVal ]
    fetch("/musicGeneration",
      {
        method: "POST",
        body: values ,
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
            <Select value={ddValue} onChange={handleDDchange} multiple>
                <MenuItem value={"A"}>A</MenuItem>
                <MenuItem value={"B"}>B</MenuItem>
                <MenuItem value={"C"}>C</MenuItem>
                <MenuItem value={"D"}>D</MenuItem>
                <MenuItem value={"E"}>E</MenuItem>
                <MenuItem value={"F"}>F</MenuItem>
                <MenuItem value={"G"}>G</MenuItem>

                <MenuItem value={"A#"}>A#</MenuItem>
                <MenuItem value={"B#"}>B#</MenuItem>
                <MenuItem value={"C#"}>C#</MenuItem>
                <MenuItem value={"D#"}>D#</MenuItem>
                <MenuItem value={"E#"}>E#</MenuItem>
                <MenuItem value={"F#"}>F#</MenuItem>
                <MenuItem value={"G#"}>G#</MenuItem>

                <MenuItem value={"A-"}>A-</MenuItem>
                <MenuItem value={"B-"}>B-</MenuItem>
                <MenuItem value={"C-"}>C-</MenuItem>
                <MenuItem value={"D-"}>D-</MenuItem>
                <MenuItem value={"E-"}>E-</MenuItem>
                <MenuItem value={"F-"}>F-</MenuItem>
                <MenuItem value={"G-"}>G-</MenuItem>
            </Select> 
            
            <Button onClick={upload}>Upload</Button>
        </Grid>
    }

    </div>
    );
}
export default Generation;


