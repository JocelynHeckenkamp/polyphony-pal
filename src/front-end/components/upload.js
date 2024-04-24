import React, { useState } from 'react';
import { Typography, Button, Grid, Paper, Snackbar, Alert, CircularProgress } from '@mui/material';
import css from "./frontEnd.module.css"
import { HOST } from '../utils';

function Upload({ titleTXT, subTXT, thirdTXT, setVis, setXML, setLoading, setMusicErrors, setMusicSuggestions }) {
  const resultsRoute = "/results";
  const [file, setFile] = useState(null);
  const [loading, setLoadingState] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [error, setError] = useState(false);

  const handleUpload = async () => {
    try {
      if (!file) {
        setSnackbarMessage("No file selected");
        setError(true);
        setSnackbarOpen(true);
        return;
      }
      if(window.location.href.includes(resultsRoute)){
        setLoading(true);
        // Upload file to the backend for error checking
        const res = await fetch(`${HOST}/upload`, {
          method: "PUT",
          body: file,
        });
        const data = await res.json();
        setMusicErrors(data.errors);
        setMusicSuggestions(data.suggestions);
        setXML(await file.text());
        setVis(false);
        // Now handle MIDI conversion
        const formData = new FormData();
        formData.append("file", file);
        const midiRes = await fetch("https://meigarage.edirom.de/ege-webservice/Conversions/musicxml-partwise%3Atext%3Axml/musicxml-timewise%3Atext%3Axml/mei30%3Atext%3Axml/mei40%3Atext%3Axml/midi%3Aaudio%3Ax-midi/", {
          method: 'POST',
          body: formData,
          redirect: 'follow'
        });
        if (midiRes.ok) {
          const blob = await midiRes.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = "converted_file.mid";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
          setSnackbarMessage("File successfully converted and downloaded!");
          setError(false);
        } else {
          throw new Error('Network response was not ok for MIDI conversion');
        }
      } else {
        fetch(`${HOST}/counterpoint`,
        {
          method: "PUT",
          body: file,
        })
        .then(response => response.text())
        .then(data => {
          //hide upload component, then set data
          //ndata[0] holds the musicXML, the rest of the array holds the errors
          
          setVis(false);
          setXML(data);

          
          //set loading bar false AFTER data has been set
        })
        .then(setLoading(false))
      }
    } catch (error) {
      console.error("Error during the upload and conversion process:", error);
      setSnackbarMessage("Failed to process the file.");
      setError(true);
    } finally {
      setLoading(false);
      setSnackbarOpen(true);
    }
  }

  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <div>
      <Grid container mt={{ xs: 20, sm: 20, md: 20, lg: 20, xl: 20 }} align="center" className={css.flex_container}>
        <Paper className={css.upload_paper} elevation={3}>
          <Typography className={css.upload_title}>{titleTXT}</Typography>
          <Typography className={css.upload_subtitle}>{subTXT}</Typography>
          <Typography className={css.upload_thirdtitle}>{thirdTXT}</Typography>
          <Grid container item direction="row" spacing={3} className={css.flex_container}>
            <Grid item>
              <input className={css.file_select} onChange={(e) => setFile(e.target.files[0])} type='file' accept='.musicxml,.mxml, .mxl'></input>
            </Grid>
            <Grid item>
              <Button variant="contained" sx={{ mt: -1 }} onClick={handleUpload} className={css.btn} disabled={loading}>
                {loading ? <CircularProgress size={24} /> : 'Upload'}
              </Button>
            </Grid>
          </Grid>
          <Snackbar open={snackbarOpen} autoHideDuration={6000} onClose={handleSnackbarClose}>
            <Alert onClose={handleSnackbarClose} severity={error ? "error" : "success"} sx={{ width: '100%' }}>
              {snackbarMessage}
            </Alert>
          </Snackbar>
        </Paper>
      </Grid>
    </div>
  );
}

export default Upload;



// import React, { useState } from 'react';
// import { Typography, Button, Grid, Paper, FormGroup, Checkbox, FormControlLabel } from '@mui/material';
// import css from "./frontEnd.module.css"
// import CustomSwitch from './customswitch';
// import { HOST } from '../utils';



// function Upload({titleTXT, subTXT, thirdTXT, setVis, setXML, setLoading, setMusicErrors, setMusicSuggestions} ) {
//   const resultsRoute = "/results"
//   const counterpointRoute = "/counterpoint"

//   const [file, setFile] = useState(null);

//   const handleUpload = async () => {
//     try {
//       if (!file) {
//         console.log("No file selected");
//         return;
//       }
//       if(window.location.href.includes(resultsRoute)){
        
//         //upload file to backend
//         //update visible components as well
//         const res = await fetch(`${HOST}/upload`,
//           {
//             method: "PUT",
//             body: file,
//           })
        
//         let data = await res.json()
//         console.log("data:", data)

//         setMusicErrors(data.errors);
//         setMusicSuggestions(data.suggestions);
//         setVis(false);
//         setXML(await file.text());
//         setLoading(false)
//       }
//       else{
//         fetch(`${HOST}/counterpoint`,
//           {
//             method: "PUT",
//             body: file,
//           })
//           .then(response => response.text())
//           .then(data => {
//             //hide upload component, then set data
//             //ndata[0] holds the musicXML, the rest of the array holds the errors
           
//             setVis(false);
//             setXML(data);
  
            
//             //set loading bar false AFTER data has been set
//           })
//           .then(setLoading(false))
//       }

//     }
//     catch(error) {
//       console.error("Error during the upload process:", error) 
//     }
//   }
  
  

//   return (

    
//     <div   >
    
//       <Grid container mt={{xs:20, sm:20, md:20, lg:20 , xl:20}} align="center" className={css.flex_container}>
        
//           <Paper className={css.upload_paper} elevation={3} >

//             <Typography className={css.upload_title} >{titleTXT}</Typography>
//             <Typography className={css.upload_subtitle} >{subTXT}</Typography>
//             <Typography className={css.upload_thirdtitle} >{thirdTXT}</Typography>
//           <Grid container item direction="row" spacing={3} className={css.flex_container}>
              
//               <Grid item>
//               <input className={css.file_select} onChange={(e) => { setFile(e.target.files[0]) }} type='file' accept='.musicxml,.mxml, .mxl' ></input>
//               </Grid>
//               <Grid item>
//               {window.location.pathname == counterpointRoute && (
//                 <CustomSwitch />)}
//               </Grid>
//             <Grid item>
//               <Button variant="contained" sx={{mt:-1}} onClick={handleUpload} className={css.btn}>Upload</Button>
//               </Grid>
//           </Grid>
//           </Paper>
        
//       </Grid>

      
//     </div>
    
    
    
//   );


// }

// export default Upload;
