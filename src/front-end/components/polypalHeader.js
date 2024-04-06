import React from 'react';
import {  Button, Grid } from '@mui/material';
import logo from '../../polypalLogo.svg';

function Header()
{
    return(
      <Grid container  className="top-bar" >
      <Grid item  xs={2} md={2} lg={2} mt={-6} justifyContent="flex-start" >

        <img src={logo} alt="polypal logo"  style={{ width: "200px", height: "200px" }}  />
      </Grid>

      <Grid item xs={7} md={7} lg={7}> </Grid>
      <Grid item xs={3} md={3} lg={3} pt={4}  className="navigation-buttons" >
        <Button size="large" sx={{ color: "black" }}>About</Button>
        <Button size="large" sx={{ color: "black" }}>Generation</Button>
        <Button size="large" sx={{ color: "black" }}>Account</Button>
        <Button size="large" sx={{ color: "black" }}>Upload</Button>
      </Grid>
  </Grid>
    );
}
export default Header;