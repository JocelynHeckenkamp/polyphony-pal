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
 const [uploadVis, setUploadVis] = useState(true);
 const [musicErrors, setMusicErrors] = useState([]);//contains array of music errors
 const [musicXml, setMusicXml] = useState('');
 const [checked, setChecked] = useState(true);  
      
 const handleChange = (event) => {
    setChecked(event.target.checked);
  };


const renderContent= () =>{
    if(isLoading){
        return(<CircularProgress/>);
    }
    if(musicXml){
        {console.log(JSON.parse(musicXml)[0])}
        return(<SheetMusicComponent musicXml={JSON.parse(musicXml)[0]}/>);
    }

    else{
            return(
            <Grid>
            <Upload titleTXT={title} subTXT={subtitle} thirdTXT={thirdtitle} setVis={setUploadVis}
            setXML={setMusicXml} setLoading={setIsLoading} setMusicErrors={setMusicErrors} />
            <Checkbox checked={checked} onChange={handleChange} inputProps={{ 'aria-label': 'controlled' }} label="Joe"> </Checkbox>
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