import axios from 'axios';
import React, { Component } from 'react';
import { Switch, Redirect, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../constants';

import RequestCategory from './RequestCategory';

export default class Request extends Component {
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

    const routes = [];

    const renderItemTypeForCategory = (category) => (itemType) => {
      const path = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ path } key={ path }>
          <h2>Placeholder for: { itemType }</h2>
        </Route>
      );
    };

    for (var category in itemTypesByCategory) {
      routes.push(
          <Route exact path={ paths[category] } key={ paths[category] }>
            <RequestCategory category={ category } requests={ requests } paths={ paths } />
          </Route>
      )

      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);
    }

    return (
      <div id="request-container">
        <Switch>
          { routes }
          <Redirect to={ paths.clothing }/>
        </Switch>
      </div>
    )
  }
};
