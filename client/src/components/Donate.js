import axios from 'axios';
import React, { Component } from 'react';
import { Switch, Redirect, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../constants';
import DonateCategory from './DonateCategory';
import DonateItemsTable from './DonateItemsTable';
import FulfillmentForm from './FulfillmentForm';

class DonationDetail extends Component {
  render() {
    const { requests } = this.props;
    const matchParams = this.props.match.params;

    const requestsById = {};

    if (requests) {
      requests.forEach(
        request => {
          requestsById[request.id] = request;
        }
      );

      const request = requestsById[matchParams.id];

      if (request) {
        return (
          <FulfillmentForm request={ request } />
        );
      }
    }

      return null;
  }
}


export default class Donate extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requests: null
    };
  }

  componentDidMount() {
    axios.get('/api/requests/')
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

    const renderItemTypeForCategory = (category) => (itemType) => {
      const itemTypePath = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ itemTypePath } key={ itemTypePath }>
          <DonateItemsTable itemType={ itemType } category={ category } requests={ requests } paths={ paths } />
        </Route>
      );
    }

    for (var category in itemTypesByCategory) {
      routes.push(
        <Route exact path={ paths[category] } key={ paths[category] }>
          <DonateCategory category={ category } requests={ requests } paths={ paths } />
        </Route>
      );

      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);
    }

    const requestPath = "/donate/:id";

    routes.push(
      <Route exact path={ requestPath } key={ requestPath } render={ props => <DonationDetail {...props} requests={ requests } /> }/ >
    );

    return (
      <div id="donate-container">
        <Switch>
          { routes }
          <Redirect to={ paths.clothing }/>
        </Switch>
      </div>
    )
  }
};
