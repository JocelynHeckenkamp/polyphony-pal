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
            setShowXMLtoMIDI(true); // Set state to true to render XMLtoMIDI component
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
                    <Grid container spacing={2} sx={{ display: 'flex', justifyContent: 'center', padding: "10px" }} className={css.flex_container}>
                        <Grid container item direction="column" sx={{ overflow: 'visible', width: '40vw' }}>
                            <Paper sx={{ pt: 5, backgroundColor: "#ffffff", borderRadius: 5, width: "100%" }} elevation={4} onClick={handleClick}>
                                <Grid sx={{ justifyContent: 'center' }}>
                                    <SheetMusicComponent musicXml={musicXml} />
                                </Grid>
                            </Paper>
                            {showXMLtoMIDI && <XMLtoMIDI musicXML={musicXml} />} {/* Render XMLtoMIDI component conditionally */}
                        </Grid>

                        <Grid container item sx={{ maxHeight: '80vh', maxWidth: '15vw' }}>
                            <Typography>Errors</Typography>
                            <Grid container item className={css.error_scroller}>
                                {musicErrors.map((error, index) => (
                                    <Grid item pb={2} pr={2} key={index}>
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

                        <Grid container item sx={{ maxHeight: '80vh', maxWidth: '15vw' }}>
                            <Typography>Suggestions</Typography>
                            <Grid container item className={css.error_scroller}>
                                {musicSuggestions.map((error, index) => (
                                    <Grid item pb={2} pr={2} key={index}>
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

                        <Grid container item sx={{ maxHeight: '80vh', maxWidth: '15vw' }}>
                            <Typography>Suggestions</Typography>
                            <Paper sx={{ padding: 3, backgroundColor: "#ffffff", borderRadius: 5, width: "10vw", ml: 2 }} elevation={2} >
                                <Typography>Number of Errors: {musicErrors.length}</Typography>
                            </Paper>
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