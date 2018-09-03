import React, { Component } from 'react'


class Ribbon extends Component {
  render() {
    return <div class="beta-corner-ribbon">Demo</div>;
  }
}

class Banner extends Component {
  // Currently not being used (but alternative to ribbon)
  render() {
    return <div class="beta-banner">This is just a demo</div>;
  }
}


export default class BetaInfo extends Component {
  render() {
    return <div>
      <Ribbon />
    </div>
  }
}
