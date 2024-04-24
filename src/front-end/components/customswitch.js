import React, { useState } from 'react';
import { Typography, Switch, Grid, styled, alpha, FormGroup, FormControlLabel, FormControl } from '@mui/material';
import css from "./frontEnd.module.css"

function CustomSwitch({switchVal}){
    
const [switchState, setSwitch] = useState(false);

    const Custom = styled(Switch)(({ theme }) => ({
        '& .MuiSwitch-switchBase.Mui-checked': {
          color: "#1c1b1c",
          '&:hover': {
            backgroundColor: alpha("#1c1b1c", theme.palette.action.hoverOpacity),
          },
        },
        '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
          backgroundColor: "#1c1b1c",
        },
      }));

const handleChange = (e) => {
    //if checked, setval to melody. else harmony
    
    setSwitch(e.target.checked)
   if(e.target.checked){
    switchVal("Harmony");
    
   }
   else{switchVal("Melody")
   
   }
   
}



return(
<div >

   <Grid container className={css.switch_container}>
    <Typography className={css.switch_text}>Melody</Typography>

    
    <Custom className={css.switch} checked={switchState} onClick={handleChange} ></Custom>
      

    <Typography className={css.switch_text} sx={{mr:5}}>Harmony</Typography>
    </Grid>
</div>);    
}
export default CustomSwitch;