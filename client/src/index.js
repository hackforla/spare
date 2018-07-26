import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

// Import bootstrap styles
import 'bootstrap/dist/css/bootstrap.css';

//style sheets
import './css/index.css';

//components dir
import App from './components/App.js';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render((
  <BrowserRouter>
    <App />
  </BrowserRouter>
), document.getElementById('root')
);
registerServiceWorker();
