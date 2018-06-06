import axios from 'axios';
import React, { Component } from 'react';
import { Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Switch, Redirect, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../constants';
import DonateCategory from './DonateCategory';
import DonateItemsTable from './DonateItemsTable';


export default class Donate extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    axios.get('http://localhost:8000/api/requests/')
      .then((res) => {
        this.setState((oldState) => ({
          requests: res.data
        }));
      })
      .catch((err) => {
        this.setState((oldState) => ({alert: 'danger', message: 'Unable to get donation data. Please try again later.'}));
        console.log(err)
      });
  }

  render() {
    const { match } = this.props;
    const { requests } = this.state;

    const paths = {
      'clothing': match.path + '/clothing',
      'essentials': match.path + '/essentials',
      'hygiene': match.path + '/hygiene',
      'donate': '/donate',
      'request': '/request',
    };

    let routes = [];
    for (var category in itemTypesByCategory) {
      routes.push(
        <Route exact path={ paths[category] } key={ paths[category] }>
          <DonateCategory category={ category } requests={ requests } paths={ paths } />
        </Route>
      );

      itemTypesByCategory[category].forEach((itemType) => {
        const path = paths[category] + '/' + itemType + '/';
        routes.push(
          <Route exact path={ path } key={ path }>
            <div>
              <DonateItemsTable itemType={ itemType } category={ category } requests={ requests } paths={ paths } />
            </div>
          </Route>
        );
      })
    }

    return (
      <div>
        <LinkContainer to={ paths.request }>
          <Button>Request an item</Button>
        </LinkContainer>
        <Switch>
          { routes }
          <Redirect to={ paths.clothing }/>
        </Switch>
      </div>
    )
  }
};
