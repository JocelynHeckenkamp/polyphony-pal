import React from 'react';
import {  Button, Grid, Link } from '@mui/material';
import logo from '../../polypalLogo.svg';

function Header()
{
    return(
    <Grid container  className="top-bar" >
      <Grid item  xs={2} md={2} lg={2} mt={-6}  >

      <Link href="/"><img src={logo} alt="polypal logo"  style={{ width: "200px", height: "200px" }}  /></Link>
      </Grid>

<<<<<<< HEAD
      <Grid item xs={7} md={7} lg={7}> </Grid>
      <Grid item xs={3} md={3} lg={3} pt={4}  className="navigation-buttons" >
        <Button size="large" sx={{ color: "black" }}>About</Button>
        <Button size="large" sx={{ color: "black" }}>Generation</Button>
        <Button size="large" sx={{ color: "black" }}>Account</Button>
        <Button size="large" sx={{ color: "black" }}>Upload</Button>
=======
      
      <Grid container item xs={10} md={10} lg={10} pt={4.6} className="navigation-buttons" justifyContent="end">
        <Grid item >
        <Link href="/"><Button size="large" sx={{ color: "black" }}>About</Button></Link>
        <Link href="/"><Button size="large" sx={{ color: "black" }}>Features</Button></Link>  
                        <Button size="large" sx={{ color: "black" }}>Account</Button>
        <Link href="/results"><Button size="large" sx={{ color: "black" }}>Upload</Button> </Link>
        </Grid>
>>>>>>> 97540f8902892e4d085d389e39daf5b7ab4ec09c
      </Grid>
  </Grid>
    );
}
export default Header;