import React, { Component } from 'react';
import donateLogo from "./../assets/logos/logo_spare.svg";
import requestLogo from "./../assets/logos/logo_spare_alt.svg";
import { Link, Route, Switch } from "react-router-dom";


export default class Logo extends Component {
  render() {
    return (
      <Link to="/">
        <Switch>
          <Route path="/donate">
            <img src={donateLogo} alt="Spare" className="logo"/>
          </Route>
          <Route path="/request">
            <img src={requestLogo} alt="Spare" className="logo" />
          </Route>
          <Route>
            <img src={donateLogo} alt="Spare" className="logo" />
          </Route>
        </Switch>
      </Link>
    )
  }
}
