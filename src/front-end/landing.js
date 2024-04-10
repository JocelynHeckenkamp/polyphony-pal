// import React, { useState, useEffect } from 'react';
// import { Outlet, Link } from "react-router-dom";
// import logo from '../logo.svg'
// import '../App.css';

// function Landing() {
//   const [currentTime, setCurrentTime] = useState(0);

//   useEffect(() => {
//     fetch('/time').then(res => res.json()).then(data => {
//       setCurrentTime(data.time);
//     });
//   }, []);

//   return (
//     <div className="Landing">
//       <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <h2>Welcome to React</h2>
//           <p>The current time is {currentTime}.</p>
//       </header>
//         <Link to="/upload">
//         <button >Upload</button>
//         </Link>
//       <Outlet />
//     </div>
//   );
// }

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Typography, Button, Grid, Avatar } from '@mui/material';
import logo from '../polypalLogo.svg';
import  "../Landing.css";
import {StyledEngineProvider} from "@mui/styled-engine"



function Landing() {
 

  const teamMembers = [
    { name: 'Alexander N. Chin', role: 'Software Engineer', email: 'anc202000@utdallas.edu', initials: 'AC' },
    { name: 'Aseal Mohmand', role: 'Software Engineer', email: 'asm200011@utdallas.edu', initials: 'AM' },
    { name: 'Jocelyn Heckenkamp', role: 'Software Engineer', email: 'jah190020@utdallas.edu', initials: 'JH' },
    { name: 'Cory Harris', role: 'Software Engineer', email: 'cnh200002@utdallas.edu', initials: 'CH' }
  ];

  return (
    <StyledEngineProvider injectFirst>
    
    <Container maxWidth="lg" className="landing-container">

      <Grid container spacing={4} alignItems="center" className="intro-box">

        <Grid item xs={12} md={7}>
          <Typography variant="h2" component="h1" gutterBottom className="landing-title">
            PolyphonyPal
          </Typography>
          <Typography variant="h6" color="inherit" className="landing-subtitle" sx={{ mb: 2 }}>
            Welcome to PolyphonyPal, your go-to music mistake checker!
            Perfect your compositions with ease using our intuitive platform
            based on classical counterpoint rules. Receive real-time feedback,
            visual error indicators, and customizable settings to accelerate
            your learning in music theory classes or personal practice sessions.
            With PolyphonyPal, compose confidently, correct errors swiftly, and
            elevate your musical creations to new heights of excellence.
          </Typography>
          <Button variant="contained" component={Link} to="/results" className="get-started-btn"  >
            Get Started
          </Button>
        </Grid>

        {/* Logo */}
        <Grid item xs={12} md={5} className="logo-container">
          <img src={logo} alt="PolyphonyPal logo" className="landing-logo" />
        </Grid>
      </Grid>


      <Typography variant="h4" component="div" className="team-heading">
        Meet the Team
      </Typography>
      <Grid container spacing={4} className="team-grid-container">
        {teamMembers.map((member, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index} className="team-member">
            <Avatar className="team-avatar">{member.initials}</Avatar>
            <Typography variant="subtitle1" component="div" className="team-name">
              {member.name}
            </Typography>
            <Typography color="textSecondary" className="team-role">
              {member.role}
            </Typography>
            <Typography variant="body2" color="textSecondary" className="team-email">
              {member.email}
            </Typography>
          </Grid>
        ))}
      </Grid>

    </Container>
    </StyledEngineProvider>
  );
}

export default Landing;