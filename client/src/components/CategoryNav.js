import React, { Component } from 'react';
import {Nav, NavItem } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';


export default class CategoryNav extends Component {
  render() {
    const { paths } = this.props;

    return (
      <div className="nav-container">
        <Nav bsStyle="pills" justified>
          <LinkContainer to={ paths.clothing }>
            <NavItem eventKey={'clothing'}>Clothing</NavItem>
          </LinkContainer>
          <LinkContainer to={ paths.essentials }>
            <NavItem eventKey={'essentials'}>Essentials</NavItem>
          </LinkContainer>
          <LinkContainer to={ paths.hygiene }>
            <NavItem eventKey={'hygiene'}>Hygiene</NavItem>
          </LinkContainer>
        </Nav>
      </div>
    )
  }
};
