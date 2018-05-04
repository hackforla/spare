import axios from 'axios';
import React, { Component } from 'react';
import { Button, Nav, NavItem, Row } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Switch, Redirect, Route } from 'react-router-dom';


export default class CategoryNav extends Component {
  render() {
    const { mode, paths } = this.props;

    return (
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
    )
  }
};
