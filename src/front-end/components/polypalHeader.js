import React from 'react';
import {  Button, Grid } from '@mui/material';
import logo from '../../polypalLogo.svg';

function Header()
{
    return(
    <Grid container  className="top-bar" >
      <Grid item  xs={2} md={2} lg={2} mt={-6}  >

        <img src={logo} alt="polypal logo"  style={{ width: "200px", height: "200px" }}  />
      </Grid>

      
      <Grid container item xs={10} md={10} lg={10} pt={4.6} className="navigation-buttons" justifyContent="end">
        <Grid item >
        <Button size="large" sx={{ color: "black" }}>About</Button>
        <Button size="large" sx={{ color: "black" }}>Features</Button> 
        <Button size="large" sx={{ color: "black" }}>Account</Button>
        <Button size="large" sx={{ color: "black" }}>Upload</Button>
        </Grid>
      </Grid>
  </Grid>
    );
}
export default Header;