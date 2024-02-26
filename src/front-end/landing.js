import React, { useState, useEffect } from 'react';
import { Outlet, Link } from "react-router-dom";
import logo from '../logo.svg'
import '../App.css';

function Landing() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="Landing">
      <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
          <p>The current time is {currentTime}.</p>
      </header>
        <Link to="/upload">
        <button >Upload</button>
        </Link>
      <Outlet />
    </div>
  );
}

export default Landing;