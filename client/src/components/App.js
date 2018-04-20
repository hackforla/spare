import React, { Component } from 'react'
import RequestForm from './RequestForm.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Spare</h1>
          <RequestForm/>
        </header>
      </div>
    );
  }
}

export default App;
