import React, { Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';

export default class RequestLayout extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // TODO: This should be received as a prop
      activeKey: 1
    };
  }

  handleSelect = (selectedKey) => {
    this.setState({activeKey: selectedKey})
  }

  render() {
    return (
      <div>
        <h2>Give spare items directly to people in need.</h2>
        <h2>What could you spare?</h2>
        <Nav bsStyle="pills" activeKey={this.state.activeKey} onSelect={this.handleSelect}>
          <NavItem eventKey={1} href="/donate/clothing">Clothing</NavItem>
          <NavItem eventKey={2} href="/donate/essentials">Essentials</NavItem>
          <NavItem eventKey={3} href="/donate/hygiene">Hygiene</NavItem>
        </Nav>
        {this.props.children}
      </div>
    )
  }
}
