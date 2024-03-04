
import React, {useState} from 'react';
import { Container, Typography, Button, Grid,  Paper, Card } from '@mui/material';
import { Link } from 'react-router-dom';


function Upload() {
const [file, setFile] = useState(null);
 
function handleUpload()
{
    if( !file)
    {
        console.log("No file selected");
        return;
    }
    //const fd = new FormData();
    //fd.append('file',file);

    //upload file to backend
    //change fd to file if theres an error
   fetch("/upload", 
    {
        method: "PUT",
        body: file,
    });

 
}


  return (


    <div  className="upload-container" align="left">
        <Grid container   direction="row"  className="top-bar">
          <Grid item xs={9} md={9} lg={9} >
            <Typography variant="h2" gutterBottom component="div" className="upload-title">
              PolyphonyPal
            </Typography>
          </Grid>
        
        
          <Grid item xs={3} md={3} lg={3} pt={4}     className="navigation-buttons" >
            <Button  size="large" sx={{color: "black"}}>About</Button>
            <Button size="large" sx={{color: "black"}}>Features</Button>
            <Button size="large" sx={{color: "black"}}>Account</Button>
            <Button size="large" sx={{color: "black"}}>Upload</Button>
          </Grid>
        </Grid>
        
          <Grid container  mt={30}  justifyContent="center"  className="upload-Card" >
          <Grid item align="center" >
            <Paper sx={{padding:3, backgroundColor: "#f7f7f7", px:10}} elevation={2} >
              
              <Typography variant="h2" color="black" align="center" className="upload-subtitle">
              Upload Music XML File
              </Typography>
              <Typography pb={3} pt={1} variant="h6" color="textSecondary" align="center" className="upload-subtitle">
              Export Music XML file from Musescore or any other editor
              </Typography>
              
            <input onChange={ (e) => {setFile(e.target.files[0])}} type='file' accept='.musicxml,.mxml, .mxl' align="center"></input>
            <Button variant="contained" onClick={handleUpload} sx={{backgroundColor: "black"}}>Upload</Button>
            
            </Paper>
          </Grid>
          </Grid>
        
     

      
      
        
            
            
          
       
     

    </div>
    
  );

  
}

export default Upload;

/* <div className="Upload">
        <h1>Upload Test</h1>

        <input onChange={ (e) => {setFile(e.target.files[0])}} type='file' accept='.musicxml,.mxml, .mxl' ></input>
        <Button variant="contained" onClick={handleUpload}>Upload</Button>
        
    </div> */