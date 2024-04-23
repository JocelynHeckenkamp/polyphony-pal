
import React, { useState } from 'react';
import { Typography, Button, Grid, Paper, FormGroup, Checkbox, FormControlLabel } from '@mui/material';
import css from "./frontEnd.module.css"
import CustomSwitch from './customswitch';



function Upload({titleTXT, subTXT, thirdTXT, setVis, setXML, setLoading, setMusicErrors, setMusicSuggestions} ) {
  const resultsRoute = "/results"
  const counterpointRoute = "/counterpoint"

  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    try {
      if (!file) {
        console.log("No file selected");
        return;
      }
      if(window.location.href.includes(resultsRoute)){
        
        //upload file to backend
        //update visible components as well
        const res = await fetch("/upload",
          {
            method: "PUT",
            body: file,
          })
        
        let data = await res.json()
        console.log("data:", data)

        setMusicErrors(data.errors);
        setMusicSuggestions(data.suggestions);
        setVis(false);
        setXML(await file.text());
        setLoading(false)
      }
      else{
        fetch("/counterpoint",
          {
            method: "PUT",
            body: file,
          })
          .then(response => response.text())
          .then(data => {
            //hide upload component, then set data
            //ndata[0] holds the musicXML, the rest of the array holds the errors
           
            setVis(false);
            setXML(data);
  
            
            //set loading bar false AFTER data has been set
          })
          .then(setLoading(false))
      }

    }
    catch(error) {
      console.error("Error during the upload process:", error) 
    }
  }
  
  

  return (

    
    <div   >
    
      <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}} align="center" className={css.flex_container}>
        
          <Paper className={css.upload_paper} elevation={3} >

            <Typography className={css.upload_title} >{titleTXT}</Typography>
            <Typography className={css.upload_subtitle} >{subTXT}</Typography>
            <Typography className={css.upload_thirdtitle} >{thirdTXT}</Typography>
          <Grid container item direction="row" spacing={3} className={css.flex_container}>
              
              <Grid item>
              <input className={css.file_select} onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
              </Grid>
              <Grid item>
              {window.location.pathname == counterpointRoute && (
                <CustomSwitch />)}
              </Grid>
            <Grid item>
              <Button variant="contained" sx={{mt:-1}} onClick={handleUpload} className={css.btn}>Upload</Button>
              </Grid>
          </Grid>
          </Paper>
        
      </Grid>

      
    </div>
    
    
    
  );


}

export default Upload;
