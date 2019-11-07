import React, { Component, Fragment } from "react"
import { Switch, Route } from "react-router-dom"

import asyncComponent from '../utils';

const AdminApp = asyncComponent((props) => import("./AdminApp"));
const DonorApp = asyncComponent((props) => import("./DonorApp"));

class App extends Component {
  render() {
    return (
      <Switch>
        <Route path='/staff'>
          <AdminApp />
        </Route>
        <Route>
          <DonorApp />
        </Route>
      </Switch>
    )
  }
}

export default App
