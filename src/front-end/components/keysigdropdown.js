
import React, { useState, useEffect } from 'react';
import {  Select,MenuItem, InputLabel, FormControl, OutlinedInput } from '@mui/material';


function Keydropdown ({setdrop, ddValue}){


//input label is so weird
return(
<FormControl variant="outlined" sx={{width:250}}>
<InputLabel id="Key">Key Signature</InputLabel>
<Select value={ddValue} onChange={(e) => {setdrop(e.target.value)}} input={<OutlinedInput label="Key Signature" />}  >
                    <MenuItem value={"A"}>A</MenuItem>
                    <MenuItem value={"B"}>B</MenuItem>
                    <MenuItem value={"C"}>C</MenuItem>
                    <MenuItem value={"D"}>D</MenuItem>
                    <MenuItem value={"E"}>E</MenuItem>
                    <MenuItem value={"F"}>F</MenuItem>
                    <MenuItem value={"G"}>G</MenuItem>
    
                    <MenuItem value={"A#"}>A#</MenuItem>
                    <MenuItem value={"B#"}>B#</MenuItem>
                    <MenuItem value={"C#"}>C#</MenuItem>
                    <MenuItem value={"D#"}>D#</MenuItem>
                    <MenuItem value={"E#"}>E#</MenuItem>
                    <MenuItem value={"F#"}>F#</MenuItem>
                    <MenuItem value={"G#"}>G#</MenuItem>
    
                    <MenuItem value={"A-"}>A-</MenuItem>
                    <MenuItem value={"B-"}>B-</MenuItem>
                    <MenuItem value={"C-"}>C-</MenuItem>
                    <MenuItem value={"D-"}>D-</MenuItem>
                    <MenuItem value={"E-"}>E-</MenuItem>
                    <MenuItem value={"F-"}>F-</MenuItem>
                    <MenuItem value={"G-"}>G-</MenuItem>
</Select> 
</FormControl>
);
}

export default Keydropdown;