import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Paper, Typography, Grid, Button, CircularProgress, Checkbox  } from '@mui/material';
import Upload from "./components/upload";
import Header from './components/polypalHeader';
import css from "./components/frontEnd.module.css"

function Counterpoint() {
  const title= String.raw`Upload Music XML File`; 
  const subtitle = String.raw`Export Music XML file from Musescore or any other editor`;
  const thirdtitle = String.raw`One line cantus firmus to be harmonized`

 const [isLoading, setIsLoading] = useState(false); //loading spinner state
 const [musicXml, setMusicXml] = useState();
  

  function copyContent(xml) {
     
    try {
     navigator.clipboard.writeText(xml);
     console.log('Content copied to clipboard');
      /* Resolved - text copied to clipboard successfully */
    
        console.log(alertCopy)
        setAlertCopy(true)
        setTimeout(() => {
            setAlertCopy(false);
          }, 3000);
        

    } catch (err) {
      console.error('Failed to copy: ', err);
      /* Rejected - text failed to copy to the clipboard */
    }
  }


  const renderContent = () => {
    //if waiting for fetch
    if (isLoading) {
      return (
      <>
      <CircularProgress />
      <Typography>Generating scores....Please wait a moment</Typography>
      </>);
    }
    //if returned an empty array
    if (musicXml) {
        if(musicXml.length == 0)
        {
          return(<div className={css.flex_container}>
            <Typography className={css.upload_numerals}>Incorrect input Melody/Harmony <br/> Please try again</Typography></div>);
        }
    //ran based on returned musicXMLs
    else{
      return (<>
        {console.log(musicXml)}
        <Typography className={css.upload_numerals}>Generated scores:</Typography>
      <Grid container direction="column" spacing={2}>
        
        {musicXml.map(xml => (
          <Grid item key={xml}>
            <Paper className={css.music_paper} onClick={() => { copyContent(xml) }} >
              <SheetMusicComponent musicXml={xml} />
            </Paper>
          </Grid>
        ))}
      </Grid>
      </>)
      }
      
    }

    else {
      return (
        <Grid>
          <Upload titleTXT={title} subTXT={subtitle} thirdTXT={thirdtitle}
            setXML={setMusicXml} setLoading={setIsLoading} />

        </Grid>

      );
    }


  }


    return(
    <div>
        <Header/>
        {renderContent()}


        
    </div>
    );
}

export default Counterpoint;