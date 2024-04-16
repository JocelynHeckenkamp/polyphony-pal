import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Paper, Typography, Grid, Button } from '@mui/material';
import Upload from "./components/upload";
import Header from './components/polypalHeader';
import css from "./components/frontEnd.module.css"

function Counterpoint() {


 const handleUpload = () =>{

 }     
      



const renderContent= () =>{
    return(
        <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}}  className={css.flex_container}>
        <Grid item  align="center">
          <Paper className={css.upload_paper} elevation={3}>

            <Typography className={css.upload_title} >
              Upload Music XML File
            </Typography>
            <Typography className={css.upload_subtitle} >
              This file will generate counterpoint music?
            </Typography>

            <input onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
            <Button variant="contained" onClick={handleUpload} className={css["btn"]}>Upload</Button>

          </Paper>
        </Grid>
      </Grid>

    );
}


    return(
    <div>
        <Header/>
        {renderContent()}


        <div className={css.upload_background}></div>
    </div>
    );
}

export default Counterpoint;