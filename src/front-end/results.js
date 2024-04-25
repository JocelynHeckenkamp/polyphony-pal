import React, { useState, useEffect, useMemo } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import { Paper, CircularProgress, Grid, Typography } from '@mui/material';
import Upload from "./components/upload";
import Header from './components/polypalHeader';
import css from "./components/frontEnd.module.css"
import XMLtoMIDI from './XMLtoMIDI';
import MidiPlayerComponent from './components/midiplayback';

function Results() {
    const [musicXml, setMusicXml] = useState('');
    const [midiBlob, setMidiBlob] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [pageError, setPageError] = useState(null);
    const [uploadVis, setUploadVis] = useState(true);
    const [musicErrors, setMusicErrors] = useState([]);
    const [musicSuggestions, setMusicSuggestions] = useState([]);
    const [showXMLtoMIDI, setShowXMLtoMIDI] = useState(false);

    const handleConversionComplete = (midiBlob, errorMessage) => {
        if (midiBlob) {
            setMidiBlob(midiBlob);
        } else {
            console.error(errorMessage);
            setPageError(errorMessage);
        }
    };

    const handleClick = () => {
        if (musicXml) {
            setShowXMLtoMIDI(prevShowXMLtoMIDI => !prevShowXMLtoMIDI);
        }
    };

    const renderContent = useMemo(() => {
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
                            {showXMLtoMIDI && <XMLtoMIDI musicXML={musicXml} onConversionComplete={handleConversionComplete} />}
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

                        {midiBlob && <MidiPlayerComponent midiBlob={midiBlob} />}
                    </Grid>
                </div>
            );
        } else {
            return <p>No sheet music data available.</p>;
        }
    }, [uploadVis, pageError, isLoading, musicXml, showXMLtoMIDI, musicErrors, musicSuggestions, midiBlob]);

    return (
        <div className={css.flex_container}>
            <Grid>
                <Header />
                {renderContent}
            </Grid>
        </div>
    );
}

export default Results;
