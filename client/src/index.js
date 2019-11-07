import React from 'react';
import ReactBreakpoints from 'react-breakpoints';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

// Import bootstrap styles
import 'bootstrap/dist/css/bootstrap.css';

//style sheets
import './css/index.css';

//components dir
import App from './components/App';
import registerServiceWorker from './utils/registerServiceWorker';

import { breakpoints } from './utils/constants';

ReactDOM.render((
  <BrowserRouter>
    <ReactBreakpoints breakpoints={breakpoints}>
      <App />
    </ReactBreakpoints>
  </BrowserRouter>
), document.getElementById('root')
);
registerServiceWorker();
