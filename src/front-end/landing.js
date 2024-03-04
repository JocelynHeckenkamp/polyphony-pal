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
import { Container, Typography, Button, Grid, Box, Avatar } from '@mui/material';
import logo from '../logo.svg';
import '../Landing.css';


function Landing() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time')
      .then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      });
  }, []);

  const teamMembers = [
    { name: 'Alexander N. Chin', role: 'Software Engineer', email: 'anc202000@utdallas.edu', initials: 'AC' },
    { name: 'Aseal Mohmand', role: 'Software Engineer', email: 'asm200011@utdallas.edu', initials: 'AM' },
    { name: 'Jocelyn Heckenkamp', role: 'Software Engineer', email: 'jah190020@utdallas.edu', initials: 'JH' },
    { name: 'Cory Harris', role: 'Software Engineer', email: 'cnh200002@utdallas.edu', initials: 'CH' }
  ];

  return (
    <Container maxWidth="lg" className="landing-container">
      <Box className="landing-header">
      <img src={logo} alt="logo" className="landing-logo" />
        <Typography variant="h2" gutterBottom component="div" className="landing-title">
          PolyphonyPal
        </Typography>
        <Typography variant="subtitle1" color="textSecondary" className="landing-subtitle">
          Welcome to PolyphonyPal, your go-to music mistake checker!
        </Typography>

        <Typography variant="h6" color="textSecondary" className="landing-subtitle">
          Welcome to PolyphonyPal, your go-to music mistake checker!
          Perfect your compositions with ease using our intuitive platform
          based on classical counterpoint rules. Receive real-time feedback,
          visual error indicators, and customizable settings to accelerate
          your learning in music theory classes or personal practice sessions.
          With PolyphonyPal, compose confidently, correct errors swiftly, and
          elevate your musical creations to new heights of excellence.
        </Typography>

        <Button variant="contained" component={Link} to="/get-started" className="landing-button">
          Get Started
        </Button>
      </Box>

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

      {/* Additional sections like user testimonials can be added here */}
      {/* ... */}

    </Container>
  );
}

export default Landing;