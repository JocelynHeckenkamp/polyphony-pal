
import React, { useState } from 'react';
import { Typography, Button, Grid, Paper } from '@mui/material';



function Upload({setVis, setXML, setLoading} ) {
  
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
        setVis(false);
        setXML(data);
        
        //set loading bar false AFTER data has been set
      })
      .then(setLoading(false))
      .catch(error => console.error("Error during the upload process:", error));
  }


  return (


    <div className="upload-container" align="left">
      

      <Grid container mt={30} justifyContent="center" className="upload-Card" >
        <Grid item align="center" >
          <Paper sx={{ padding: 3, backgroundColor: "#f7f7f7", px: 10 }} elevation={2} >

            <Typography variant="h2" color="black" sx={{ fontWeight: "bold" }} className="upload-subtitle">
              Upload Music XML File
            </Typography>
            <Typography pb={3} pt={1} variant="h6" color="textSecondary" className="upload-subtitle">
              Export Music XML file from Musescore or any other editor
            </Typography>

            <input onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
            <Button variant="contained" onClick={handleUpload}
              sx={{ backgroundColor: "black", '&:hover': { backgroundColor: "grey" } }}
            >Upload</Button>

          </Paper>
        </Grid>
      </Grid>


    </div>

  );


}

export default Upload;
