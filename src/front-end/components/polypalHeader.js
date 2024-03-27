import React from 'react';
import {  Button, Grid } from '@mui/material';
import logo from '../../polypalLogo.svg';

function Header()
{
    return(
        <Grid container direction="row" className="top-bar">
        <Grid item container xs={9} md={9} lg={9} direction="row" >

          <img src={logo} alt="polypal logo" />
        </Grid>


        <Grid item xs={3} md={3} lg={3} pt={4} className="navigation-buttons" >
          <Button size="large" sx={{ color: "black" }}>About</Button>
          <Button size="large" sx={{ color: "black" }}>Features</Button>
          <Button size="large" sx={{ color: "black" }}>Account</Button>
          <Button size="large" sx={{ color: "black" }}>Upload</Button>
        </Grid>
      </Grid>
    );
}
export default Header;