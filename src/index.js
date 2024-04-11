import ReactDOM from "react-dom/client";
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import {StyledEngineProvider} from "@mui/styled-engine"
// import Upload from "./front-end/upload";
import Landing from "./front-end/landing";
import Results from "./front-end/results";
import Generation from "./front-end/generation";


//Always have landing LAST in routes :)
export default function Index() {
  return (
    <StyledEngineProvider injectFirst>

    <BrowserRouter>
      <Routes>


    
          <Route path="results" element={<Results />} />
          <Route path="generation" element={<Generation />} />

          <Route path="/" element={<Landing/>} />


      </Routes>
    </BrowserRouter>
    
    </StyledEngineProvider>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Index />);