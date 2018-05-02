import React, { Component } from 'react'
import { Switch, Redirect, Route } from 'react-router-dom';
import CategoriesList from '../components/CategoriesList';
import { Grid, PageHeader } from 'react-bootstrap';


class App extends Component {
  render() {
    return (
      <Grid>
        <PageHeader>
          Spare
        </PageHeader>
        <Switch>
          <Route path='/donate' render={props => (<CategoriesList mode='donate' {...props}/>)} />
          <Redirect exact from="/" to="/donate" />
          <Route path='/request' render={props => (<CategoriesList mode='request' {...props}/>)} />
          <Route path='/code'>
            <h2>Code</h2>
          </Route>
          <Route path='/about'>
            <h2>About</h2>
          </Route>
          <Route path='/contact'>
            <h2>Contact</h2>
          </Route>
          {/* TODO: 404 not working for nested routes */ }
          <Route>
            <h2>404 Not Found</h2>
          </Route>
        </Switch>
      </Grid>
    );
  }
}

export default App;
