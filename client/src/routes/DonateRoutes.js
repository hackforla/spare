import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import Clothing from '../components/DonateComponents/D-Clothing.js';
import Essentials from '../components/DonateComponents/D-Essentials.js';
import Hygiene from '../components/DonateComponents/D-Hygiene.js';

export default class DonateRoutes extends Component {

    render() {
        return (
            <div className='routes'>
                <Switch>
                    <Route path='/clothing' component={Clothing} />
                    <Route path='/essentials' component={Essentials} />
                    <Route path='/hygiene' component={Hygiene} />
                </Switch>
            </div>
        )
    }
};