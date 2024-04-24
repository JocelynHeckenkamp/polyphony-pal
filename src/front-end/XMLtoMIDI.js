import React, { useState } from 'react';
import { Button, CircularProgress, Snackbar, Alert } from '@mui/material';

function XMLtoMIDI() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [error, setError] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Set the selected file
    setError(false); // Reset errors on new file selection
  };

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  const uploadFile = () => {
    if (!file) {
      setSnackbarMessage("Please select a MusicXML file before uploading.");
      setError(true);
      setSnackbarOpen(true);
      return;
    }

    const formData = new FormData();
    formData.append("file", file); // Append the file

    const requestOptions = {
      method: 'POST',
      body: formData,
      redirect: 'follow'
    };

    setLoading(true); // Start loading
    fetch("https://meigarage.edirom.de/ege-webservice/Conversions/musicxml-partwise%3Atext%3Axml/musicxml-timewise%3Atext%3Axml/mei30%3Atext%3Axml/mei40%3Atext%3Axml/midi%3Aaudio%3Ax-midi/", requestOptions)
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.blob(); // Assume MIDI file is returned as a blob
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "converted_file.mid"; // Name the downloaded file
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        setSnackbarMessage("File successfully converted and downloaded!");
        setError(false);
        setSnackbarOpen(true);
      })
      .catch(error => {
        console.error('Error:', error);
        setSnackbarMessage("Failed to convert the file.");
        setError(true);
        setSnackbarOpen(true);
      })
      .finally(() => {
        setLoading(false); // Stop loading irrespective of the outcome
      });
  };

  return (
    <div>
      <input
        accept=".Musicxml"
        type="file"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="contained-button-file"
      />
      <label htmlFor="contained-button-file">
        <Button variant="contained" component="span" disabled={loading}>
          Upload MusicXML to convert to MIDI
        </Button>
      </label>
      <Button onClick={uploadFile} disabled={loading || !file}>
        {loading ? <CircularProgress size={24} /> : 'Convert to MIDI'}
      </Button>
      <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
        <Alert onClose={handleSnackbarClose} severity={error ? "error" : "success"} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </div>
  );
}

export default XMLtoMIDI;
