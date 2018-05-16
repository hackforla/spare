import React, { Component } from 'react';
import DonateItemsList from './DonateItemsList';
import RequestItemsList from './RequestItemsList';




export default class ItemsList extends Component {
  render() {
    const { mode } = this.props;

    if ( mode === 'donate' ){
      return (
        <DonateItemsList {...this.props} />
      )
    }
    else if ( mode === 'request' ){
      return (
        <RequestItemsList {...this.props} />
      )
    }
  }
}
