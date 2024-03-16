import React, { useState, useEffect } from 'react';
import SheetMusicComponent from './SheetMusicComponent';
import CircularProgress from '@mui/material/CircularProgress';

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
    const [error, setError] = useState(null); //error message state
    //fetch MusicXML data - if an error occurs check to make sure this fetches on mount
    //change fetch to delayedfetch to test loading bars
    useEffect(() => {
        setIsLoading(true);//start loading spinner
        fetch("/results")
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response: (HTTP response had an error)');
                }
                return res.text()
            })
            .then(data => {
                setMusicXml(data)
                setIsLoading(false);//success stop loading spinner state
            })
            .catch(error => {
                console.error("Error fetching MusicXML:", error);
                setError('Failed to load sheet music. Please try again.');//set error message
                setIsLoading(false);//error stop loading spinner state
            });
    }, []);

    const renderContent = () => {
        if (error) {
            return <p>Error: {error}</p>;
        } else if (isLoading) {
            return <CircularProgress />;
        } else if (musicXml) { //musicXML done loading
            return <SheetMusicComponent musicXml={musicXml} />;
        } else {
            /// TODO: case of no loading but also no error and no musicXML
            return <p>No sheet music data available.</p>;
        }
    };


    return (
        <div>
            {renderContent()}
        </div>
    );
}
export default Results;
