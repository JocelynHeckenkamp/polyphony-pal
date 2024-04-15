
import React, { useState } from 'react';
import { Typography, Button, Grid, Paper } from '@mui/material';
import css from "./frontEnd.module.css"



function Upload({setVis, setXML, setLoading, setMusicErrors} ) {
  
  const [file, setFile] = useState(null);

  function handleUpload() {
    if (!file) {
      console.log("No file selected");
      return;
    }
   

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


  return (

    
    <div  >
    
      <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}}  className={css.flex_container}>
        <Grid item  align="center">
          <Paper className={css.upload_paper} elevation={3}>

            <Typography className={css.upload_title} >
              Upload Music XML File
            </Typography>
            <Typography className={css.upload_subtitle} >
              Export Music XML file from Musescore or any other editor to be analyzed
            </Typography>

            <input onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
            <Button variant="contained" onClick={handleUpload} className={css["btn"]}>Upload</Button>

          </Paper>
        </Grid>
      </Grid>

      <div className={css.upload_background}></div>
    </div>
    
    
    
  );


}

export default Upload;
