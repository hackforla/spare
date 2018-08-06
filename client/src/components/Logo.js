import React, { Component } from 'react';
import logo from "./../assets/logo/logo_spare.png";
import { Link, Route, Switch } from "react-router-dom";


export default class Logo extends Component {
  render() {
    return (
      <Switch>
        <Route path="/donate">
          <img src={logo} alt="Spare" />
        </Route>
        <Route path="/request">
          <img src={logo} alt="Spare" />
        </Route>
      </Switch>
    )
  }
}
