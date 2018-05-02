import React, { Component } from 'react';
import DonateLayout from '../DonateLayout.js';

export default class Essentials extends Component {
  render() {
    console.log(this.props);
    return (
      <DonateLayout>
        <h2>Essentials</h2>
      </DonateLayout>
    )
  }
};
