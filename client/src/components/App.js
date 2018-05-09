import React, { Component } from "react"
import { Switch, Redirect, Route } from "react-router-dom"
import Request from "./Request"
import Donate from "./Donate"
import { Grid, PageHeader, Navbar } from "react-bootstrap"
import logo from "./../assets/logo/logo_spare.png"

class App extends Component {
  render() {
    return (
      <Grid fluid={true}>
        <PageHeader>
          <div>
            <Navbar fluid={true}>
              <a href="/">
                <img src={logo} alt="" />
              </a>
            </Navbar>
          </div>
        </PageHeader>
        <div className="container">
          <Switch>
            <Route
              path="/donate"
              render={props => <Donate mode="donate" {...props} />}
            />
            <Redirect exact from="/" to="/donate" />
            <Route
              path="/request"
              render={props => <Request mode="request" {...props} />}
            />
            <Route path="/code">
              <h2>Code</h2>
            </Route>
            <Route path="/about">
              <h2>About</h2>
            </Route>
            <Route path="/contact">
              <h2>Contact</h2>
            </Route>
            {/* TODO: 404 not working for nested routes */}
            <Route>
              <h2>404 Not Found</h2>
            </Route>
          </Switch>
        </div>
      </Grid>
    )
  }
}

export default App
