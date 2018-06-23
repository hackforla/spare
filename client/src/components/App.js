import React, { Component, Fragment } from "react"
import { Switch, Redirect, Route } from "react-router-dom"
import { Grid  } from "react-bootstrap"

//Components
import Request from "./Request"
import Donate from "./Donate"
import Header from "./Header";
import About from "./About";
import Footer from "./Footer";


class App extends Component {
  render() {
    return (
      <Fragment>
        <Grid fluid={true}>
          <Header />
          <div className="container">
            <Grid>
              <Switch>
                <Route
                  path="/donate"
                  render={props => <Donate {...props} />}
                />
                <Redirect exact from="/" to="/donate" />
                <Route
                  path="/request"
                  render={props => <Request {...props} />}
                />
                <Route path="/code">
                  <h2>Code</h2>
                </Route>
                <Route path="/about">
                    <About/>
                </Route>
                <Route path="/contact">
                  <h2>Contact</h2>
                </Route>
                {/* TODO: 404 not working for nested routes */}
                <Route>
                  <h2>404 Not Found</h2>
                </Route>
              </Switch>
            </Grid>
          </div>
        </Grid>
        <Footer />
      </Fragment>
    )
  }
}

export default App
