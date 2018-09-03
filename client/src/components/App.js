import React, { Component, Fragment } from "react"
import { Switch, Redirect, Route } from "react-router-dom"
import { Grid  } from "react-bootstrap"

//Components
import Request from "./Request"
import Donate from "./Donate"
import Header from "./Header";
import About from "./About";
import Footer from "./Footer";
import BetaInfo from "./BetaInfo";
import HowItWorks from "./HowItWorks";


class App extends Component {
  render() {
    return (
      <Fragment>
        <BetaInfo />
        <Header />
        <Grid fluid={true} className="main-container">
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
              <Route path="/how-it-works">
                  <HowItWorks/>
              </Route>
              {/* TODO: 404 not working for nested routes */}
              <Route>
                <h2>404 Not Found</h2>
              </Route>
            </Switch>
          </Grid>
        </Grid>
        <Footer />
      </Fragment>
    )
  }
}

export default App
