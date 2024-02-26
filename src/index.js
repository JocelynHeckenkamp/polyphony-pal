import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import Landing from './front-end/landing';

//need to fix this router, its inefficient. (im pretty sure)
ReactDOM.render(
  <App />,
  document.getElementById('root')

 
);


ReactDOM.render(
<Landing />,
document.getElementById('landing')
);