import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Paper, CircularProgress, Grid, Typography } from '@mui/material';
import Upload from "./components/upload";
import Header from './components/polypalHeader';
import css from "./components/frontEnd.module.css"
import XMLtoMIDI from './XMLtoMIDI';  // Adjust the path as necessary




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
    const [isLoading, setIsLoading] = useState(true);
    const [pageError, setError] = useState(null);
    const [uploadVis, setUploadVis] = useState(true);
    const [musicErrors, setMusicErrors] = useState([]);
    const [musicSuggestions, setMusicSuggestions] = useState([]);
    const [showXMLtoMIDI, setShowXMLtoMIDI] = useState(false);

    const handleClick = () => {
        if (musicXml) {
            setShowXMLtoMIDI((prevShowXMLtoMIDI) => !prevShowXMLtoMIDI);
        }
    };

    const renderContent = () => {
        if (uploadVis) {
            const title = String.raw`Upload Music XML File`;
            const subtitle = String.raw`Export Music XML file from Musescore or any other editor`;
            return <Upload titleTXT={title} subTXT={subtitle} setVis={setUploadVis} setXML={setMusicXml} setLoading={setIsLoading} setMusicErrors={setMusicErrors} setMusicSuggestions={setMusicSuggestions} />;
        } else if (pageError) {
            return <p>Error: {pageError}</p>;
        } else if (isLoading) {
            return <CircularProgress />;
        } else if (musicXml) {
            return (
                <div>
                    <Grid container spacing={2}  direction="row" className={css.flex_container}>
                        <Grid  item sx={{  width: '40vw' }}>
                            <Paper className={css.music_paper} elevation={4} onClick={handleClick}>
                                
                                    <SheetMusicComponent musicXml={musicXml} />
                               
                            </Paper>
                            {showXMLtoMIDI && <XMLtoMIDI musicXML={musicXml} />} {/* Render XMLtoMIDI component conditionally */}
                        </Grid>

                        <Grid item >
                            <Typography>Errors</Typography>
                            <Grid container item className={css.error_scroller} sx={{  width: '18vw' }}>
                                {musicErrors.map((error, index) => (
                                    <Grid item pb={2} pr={1}  key={index}>
                                        <Paper sx={{ padding: 3, backgroundColor: "#ffffff", borderRadius: 5,  }} elevation={2}>
                                            Title: {error.title} <br /><br />
                                            Measure Number: {error.location[0]} <br />
                                            Offset: {error.location[1]} <br /><br />
                                            Description: {error.description} <br /><br />
                                            Suggestion: {error.suggestion}
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </Grid>

                        <Grid  item  sx={{  width: '18vw' }}>
                            <Typography>Suggestions</Typography>
                            <Grid container item className={css.error_scroller}>
                                {musicSuggestions.map((error, index) => (
                                    <Grid item pb={2} pr={1} key={index}>
                                        <Paper sx={{ padding: 3, backgroundColor: "#ffffff", borderRadius: 5 }} elevation={2}>
                                            Title: {error.title} <br /><br />
                                            Measure Number: {error.location[0]} <br />
                                            Offset: {error.location[1]} <br /><br />
                                            Description: {error.description} <br /><br />
                                            Suggestion: {error.suggestion}
                                        </Paper>
                                    </Grid>
                                ))}
                            </Grid>
                        </Grid>

                        <Grid item  >
                            <Grid  container item  direction="column" >
                                <Grid item pb={2} sx={{ maxHeight: '30vh', maxWidth: '15vw' }}>
                                    <Typography>Insights</Typography>
                                    <Paper sx={{ padding: 3, backgroundColor: "#ffffff", borderRadius: 5, width: "10vw" }} elevation={2} >
                                        <Typography>Number of Errors: {musicErrors.length}</Typography>
                                    </Paper>
                                </Grid>
                                    <Grid  item sx={{ maxHeight: '30vh', maxWidth: '15vw' }}>
                                    <Paper sx={{ padding: 3, backgroundColor: "#ffffff", borderRadius: 5, width: "10vw" }} elevation={2} >
                                        <Typography>Number of Suggestions: {musicSuggestions.length }</Typography>
                                        
                                    </Paper>
                                    </Grid>
                            </Grid>        
                        </Grid>
                        

                        {/* {musicXml && <XMLtoMIDI musicXML={musicXml} />} */}
                    </Grid>
                </div>
            );
        } else {
            return <p>No sheet music data available.</p>;
        }
    };

    return (
        <div className={css.flex_container}>
            <Grid>
                <Header />
                {renderContent()}
            </Grid>
        </div>
    );
}

export default Results;