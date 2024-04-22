import React, { useState } from 'react';
import { Typography, Switch, Grid, styled, alpha } from '@mui/material';
import css from "./frontEnd.module.css"

function CustomSwitch(){


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


return(
<div >

   <Grid container className={css.switch_container}>
    <Typography className={css.switch_text}>Melody</Typography>
    <Custom className={css.switch} ></Custom>
    <Typography className={css.switch_text}>Harmony</Typography>
    </Grid>
</div>);    
}
export default CustomSwitch;