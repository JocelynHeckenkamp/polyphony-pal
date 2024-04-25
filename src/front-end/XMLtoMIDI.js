import React, { useEffect, useCallback } from 'react';

const XMLtoMIDI = ({ musicXML, onConversionComplete }) => {
    const handleConversionComplete = useCallback((blob, error) => {
        onConversionComplete(blob, error);
    }, [onConversionComplete]);

    useEffect(() => {
        if (musicXML) {
            const xmlBlob = new Blob([musicXML], { type: 'text/xml' });
            const file = new File([xmlBlob], "input.xml", { type: 'text/xml' });
            const formData = new FormData();
            formData.append("file", file);
            fetch("https://meigarage.edirom.de/ege-webservice/Conversions/musicxml-partwise%3Atext%3Axml/musicxml-timewise%3Atext%3Axml/mei30%3Atext%3Axml/mei40%3Atext%3Axml/midi%3Aaudio%3Ax-midi/", {
                method: 'POST',
                body: formData,
                redirect: 'follow'
            })
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    } else {
                        throw new Error('Failed to convert XML to MIDI. Server responded with status: ' + response.status);
                    }
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = "converted_file.mid";
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);

                    handleConversionComplete(blob);
                })
                .catch(err => {
                    handleConversionComplete(null, err.message);
                });
        }
    }, [musicXML, handleConversionComplete]);

    return null;
};

export default XMLtoMIDI;
