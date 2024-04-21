
import React, { useState } from 'react';
import { Typography, Button, Grid, Paper, FormGroup, Checkbox, FormControlLabel } from '@mui/material';
import css from "./frontEnd.module.css"



function Upload({titleTXT, subTXT, thirdTXT, setVis, setXML, setLoading, setMusicErrors} ) {
  const resultsRoute = "/results"
  const counterpointRoute = "/counterpoint"

  const [file, setFile] = useState(null);

  function handleUpload() {
    if (!file) {
      console.log("No file selected");
      return;
    }
   if(window.location.href.includes(resultsRoute)){
      
      //upload file to backend
      //update visible components as well
      fetch("/upload",
        {
          method: "PUT",
          body: file,
        })
        .then(response => response.text())
        .then(data => {
          //hide upload component, then set data
          //ndata[0] holds the musicXML, the rest of the array holds the errors
          var errors_str = data.split("[{")[1]
          var ndata = errors_str.substring(0, errors_str.length - 2).split("}, {")
          var errorJSON = ndata.map((str) => "{" + str + "}")

          //converts the strings to JSON format
          .map((str) => str.replaceAll("'", "\"").replaceAll("(", "[").replaceAll(")", "]").toLowerCase())
          .map(JSON.parse)
          setMusicErrors(errorJSON);
          setVis(false);
          setXML(data);

          console.log(errorJSON)
          //set loading bar false AFTER data has been set
        })
        .then(setLoading(false))
        .catch(error => console.error("Error during the upload process:", error));
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
        .catch(error => console.error("Error during the upload process:", error));
    }
  }
  
  

  return (

    
    <div  >
    
      <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}} align="center" className={css.flex_container}>
        
          <Paper className={css.upload_paper} elevation={3}>

            <Typography className={css.upload_title} >{titleTXT}</Typography>
            <Typography className={css.upload_subtitle} >{subTXT}</Typography>
            <Typography className={css.upload_thirdtitle} >{thirdTXT}</Typography>
          <Grid container item direction="row" className={css.flex_container}>
              
            
              <input onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
            
              {window.location.pathname == counterpointRoute ?
                
                <FormGroup sx={{width:"fit-content"}} >
                <FormControlLabel   control={<Checkbox  defaultChecked  size="small"/>} label="Melody" />
                <FormControlLabel  control={<Checkbox size="small" />} label="Harmony" />
                </FormGroup>
                :null}
            <Grid item>
              <Button variant="contained"  onClick={handleUpload} className={css.btn}>Upload</Button>
              </Grid>
          </Grid>
          </Paper>
        
      </Grid>

      <div className={css.upload_background}></div>
    </div>
    
    
    
  );


}

export default Upload;
