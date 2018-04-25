import React, { Component } from 'react';
import { Nav, NavItem } from 'react-bootstrap';
import DonateRoutes from '../routes/DonateRoutes.js';

export default class DonateItems extends Component {
    state = {

    }

    render() {
        return (
            <div>
                <h2>Give spare items directly to people in need.</h2>
                <h2>What could you spare?</h2>
                <Nav bsStyle="tabs" activeKey={1}>
                    <NavItem eventKey={1} href="/clothing">Clothing</NavItem>
                    <NavItem eventKey={2} href="/essentials">Essentials</NavItem>
                    <NavItem eventKey={3} href="/hygiene">Hygiene</NavItem>
                </Nav>
                <DonateRoutes />
            </div>
        )
    }
}