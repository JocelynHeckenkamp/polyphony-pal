import React, { useState } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { TextField,  Paper, Grid, CircularProgress, Typography, Button } from '@mui/material';
import Header from './components/polypalHeader';
import Keydropdown from './components/keysigdropdown';
import css from "./components/frontEnd.module.css"


function Generation(){
    //ddvalue = key
    //text value = roman numerals
    const [ddValue, setDD] = useState('');
    const [textVal, setTextVal] = useState("");
    //false = spinner not showing
    const [spinner, setSpinner] = useState(false);
    const [musicXML, setMusicXML] = useState('');

const handleTextChange = (e) => {
    setTextVal(e.target.value);
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
      .then(setSpinner(true))
      .then(response => response.text())
      .then(data => {
        setMusicXML(data);
        setSpinner(false);
        //set loading bar false AFTER data has been set
      })
      .catch(error => console.error("Error during the upload process:", error));
  }
//once music is set, render
//drop down to be removed!


const render_content = () =>
{   
    if(spinner){ //if waiting on data, show spinner
        return(<CircularProgress/>);
    }
    else{
        if(musicXML){//if data is recieved, render it
            return(
             <Paper className={css.music_paper}> 
               
            <SheetMusicComponent musicXml={musicXML} /></Paper> );
        }
        else{//wait for user input
            const titleTXT ="Generate Music"
            const subTXT ="Input chords/roman numerals and key signature"
            const thirdTXT ="Please enter a comma separated list ex) I,ii,V7,I"
            return(
                <Grid>

                    <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}}  className={css.flex_container}>
                            <Grid item  align="center">
                            <Paper className={css.upload_paper} elevation={3}>

                                <Typography className={css.upload_title} >{titleTXT}</Typography>
                                <Typography className={css.upload_subtitle} >{subTXT}</Typography>
                                <Typography className={css.upload_thirdtitle} >{thirdTXT}</Typography>
                                
                                <TextField id="outlined-basic" label="Roman Numerals" variant="outlined" value={textVal} onChange={handleTextChange}/>
                                <Keydropdown setdrop={setDD} ddValue={ddValue}/>
                                <Button onClick={upload} className={css.btnLG}>Upload</Button>
 
                            </Paper>
                            </Grid>
                        </Grid>
                
               
               
                
            </Grid>
            );
        }
    }

}
    return(
        <div>
            <Header/>
            {render_content()}
            <div className={css.upload_background}></div>
        </div>
    );
}
export default Generation;


