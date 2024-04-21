import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Paper, CircularProgress, Grid } from '@mui/material';
import Upload from "./components/upload";
import Header from './components/polypalHeader';
import css from "./components/frontEnd.module.css"



//DONT DELETE
//delay fetch to test loading bars
// const delayedfetch = (url, options, delay = 10000) => new Promise((resolve, reject) => {
//     setTimeout(() => {
//         fetch(url, options)
//             .then(resolve)
//             .catch(reject);
//     }, delay);
// });


//fetch musicXML data to give to SheetMusicComponent
function Results() {
    const [musicXml, setMusicXml] = useState('');
    const [isLoading, setIsLoading] = useState(true); //loading spinner state
    const [pageError, setError] = useState(null); //error message state
    const [uploadVis, setUploadVis] = useState(true);
    const [musicErrors, setMusicErrors] = useState([]);//contains array of music errors
    

    const renderContent = () => {
        if(uploadVis){
            const title= String.raw`Upload Music XML File`; 
            const subtitle = String.raw`Export Music XML file from Musescore or any other editor`;
            return <Upload titleTXT={title} subTXT={subtitle} setVis={setUploadVis} setXML={setMusicXml}
                     setLoading={setIsLoading} setMusicErrors={setMusicErrors} />;
        }
        else{    
            if (pageError) {
                return <p>Error: {error}</p>;
            } else if (isLoading) {
                return(<CircularProgress />);
            } else if (musicXml) { //musicXML done loading
                return(
                <div > 
                <Grid container spacing={2}>  
                    <Grid container item xs={7} sm={7} md={7} lg={7} xl={7} direction="column"   sx={{ overflow: 'visible'}} >
                        <Grid item mt={-2}>
                            <Paper  sx={{  pt:5, backgroundColor: "#e0e0e0", borderRadius: 5,  }} elevation={4} >
                            <SheetMusicComponent musicXml={musicXml} />
                            </Paper>
                        </Grid>
                    </Grid>
                    
                    <Grid item xs={1} sm={1} md={1} lg={1} xl={1}></Grid>


                    <Grid container item   className={css.error_scroller} >
                        {musicErrors.map((error) => ( 
                        <Grid item pb={2} pr={2} key={musicErrors.indexOf(error)}>
                        <Paper sx={{ padding: 3,  backgroundColor: "#e0e0e0", borderRadius: 5 }} elevation={2} >
                           Title: {error.title} <br/><br/> 
                           Measure Number: {error.location[0]} <br/>
                           Offset:{error.location[1]} <br/><br/> 
                           Description: {error.description} <br/><br/> 
                           Suggestion: {error.suggestion} 
                        </Paper>
                        </Grid>

                        ))}
                   

                   <div  className={css.flex_container}> </div>
                    </Grid>
                </Grid>  
                </div>  
                );
            } else {
                /// TODO: case of no loading but also no error and no musicXML
                return <p>No sheet music data available.</p>;
            }
        }    
        
    };


    return (
        <div  className={css.flex_container}>
         
          
        <Grid >
         
             <Header />
            
            {renderContent()}
        </Grid>
        
        
        </div>
       
    );
}
export default Results;
