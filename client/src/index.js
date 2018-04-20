import React from 'react';
import ReactDOM from 'react-dom';

//bootstrap
import './css/bootstrap.css';
import './css/bootstrap-theme.css';

//style sheets
import './css/index.css';

//components dir
import App from './components/App.js';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
