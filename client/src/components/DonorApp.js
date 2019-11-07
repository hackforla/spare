import React, { Component, Fragment } from "react"
import { Switch, Route } from "react-router-dom"
import { Grid  } from "react-bootstrap"

import Request from "./Request"
import Donate from "./Donate"
import Header from "./Header";
import Home from "./Home";
import About from "./About";
import Footer from "./Footer";
import HowItWorks from "./HowItWorks";
import PrivacyPolicy from './PrivacyPolicy';
import TermsOfService from './TermsOfService';
import FrequentlyAskedQuestions from "./FrequentlyAskedQuestions";
import ScrollToTop from './ScrollToTop';

import { BasketProvider } from '../providers/BasketProvider';


class DonorApp extends Component {
  render() {
    return (
      <BasketProvider>
        <Fragment>
          <Header />
          <Grid fluid={true} className="main-container">
            <Grid>
              <Switch>
                <Route exact path='/'>
                  <Home />
                </Route>
                <Route
                  path="/donate"
                  render={props => <Donate {...props} />}
                />
                <Route
                  path="/request"
                  render={props => <Request {...props} />}
                />
                <Route path="/about">
                  <About/>
                </Route>
                <Route path='/privacy-policy'>
                  <PrivacyPolicy />
                </Route>
                <Route path='/terms-of-service'>
                  <TermsOfService />
                </Route>
                <Route path="/how-it-works">
                  <HowItWorks/>
                </Route>
                <Route path="/faqs">
                  <FrequentlyAskedQuestions/>
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
        <ScrollToTop />
      </BasketProvider>
    )
  }
}

export default DonorApp
