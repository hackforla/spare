import React from 'react';
import ReactBreakpoints from 'react-breakpoints';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

// Import bootstrap styles
import 'bootstrap/dist/css/bootstrap.css';

//style sheets
import './css/index.css';

//components dir
import App from './components/App.js';
import registerServiceWorker from './registerServiceWorker';

import { breakpoints } from './constants';

ReactDOM.render((
  <BrowserRouter>
    <ReactBreakpoints breakpoints={breakpoints}>
      <App />
    </ReactBreakpoints>
  </BrowserRouter>
), document.getElementById('root')
);
registerServiceWorker();
