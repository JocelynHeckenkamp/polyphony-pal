import React, { useState } from 'react';
import { Typography, Button, Grid, Paper, Snackbar, Alert, CircularProgress } from '@mui/material';
// import { Typography, Button, Grid, Paper, FormGroup, Checkbox, FormControlLabel } from '@mui/material';
import css from "./frontEnd.module.css"
import { HOST } from '../utils';
import CustomSwitch from './customswitch';

function Upload({ titleTXT, subTXT, thirdTXT, setVis, setXML, setLoading, setMusicErrors, setMusicSuggestions }) {
  const resultsRoute = "/results"
  const counterpointRoute = "/counterpoint"
  const [file, setFile] = useState(null);
  const[ counterpointType, setCounterpointType] = useState("Melody");
  const [loading, setLoadingState] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [error, setError] = useState(false);


  const handleUpload = async () => {
    
    try {

      if (!file) {
        setSnackbarMessage("No file selected");
        setError(true);
        setSnackbarOpen(true);
        return;
      }
      const formData = new FormData();
      formData.append("xml", file);
      formData.append("type", counterpointType);

      if(window.location.href.includes(resultsRoute)){
         setLoading(true);
        // Upload file to the backend for error checking
        const res = await fetch(`${HOST}/upload`, {
          method: "PUT",
          body: file,
        });
        const data = await res.json();
        setMusicErrors(data.errors);
        setMusicSuggestions(data.suggestions);
        setXML(await file.text());
        setVis(false);
        
      } else {
        
        setLoading(true);
       const res = await fetch(`${HOST}/counterpoint`,
          {
            method: "PUT",
            body: formData,
          });
          const data = await res.json();
          setXML(await data);
          
          
      }
    } catch (error) {
      console.error("Error during the upload and conversion process:", error);
      setError(true);
    } finally {
      setLoading(false);
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
              {window.location.pathname == counterpointRoute && (
                <CustomSwitch switchVal={setCounterpointType} />)}
              </Grid>
              <Grid item>
              <input className={css.file_select} onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
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
