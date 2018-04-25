import React, { Component } from 'react'
import RequestForm from './RequestForm.js';
import DonateItems from './DonateItems.js';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Spare</h1>
          <RequestForm />
          <DonateItems />
        </header>
      </div>
    );
  }
}

export default App;
