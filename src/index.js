import ReactDOM from "react-dom/client";
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
// import Upload from "./front-end/upload";
import Landing from "./front-end/landing";
import Results from "./front-end/results";
import Generation from "./front-end/generation";


//Always have landing LAST in routes :)
export default function Index() {
  return (
    <BrowserRouter>
      <Routes>


          {/* <Route path="upload" element={<Upload />} /> */}
          <Route path="results" element={<Results />} />
          <Route path="generation" element={<Generation />} />

          <Route path="/" element={<Landing/>} />


      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Index />);