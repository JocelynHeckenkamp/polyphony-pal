import ReactDOM from "react-dom/client";
import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "./front-end/upload";
import Landing from "./front-end/landing";
import App from "./App";

//Always have landing LAST in routes :)
export default function Index() {
  return (
    <BrowserRouter>
      <Routes>
        
          
          <Route path="upload" element={<Upload />} />
          <Route  path="app" element={<App />} />
          <Route path="/" element={<Landing/>}>
          
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Index />);