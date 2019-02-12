import React, { Component } from 'react';
import { Col, Row } from 'react-bootstrap';
import { Switch, Redirect, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../utils/constants';

import RequestForm from './RequestForm';
import RequestCategory from './RequestCategory';

export default class Request extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { match } = this.props;

    const paths = {
    'clothing': match.path + '/clothing',
      'essentials': match.path + '/essentials',
      'hygiene': match.path + '/hygiene',
      'donate': '/donate',
      'request': '/request',
    };

    const routes = [];
    const requestCategories = [];

    const renderItemTypeForCategory = (category) => (itemType) => {
      const path = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ path } key={ path }>
          <RequestForm itemType={ itemType }/>
        </Route>
      );
    };

    for (var category in itemTypesByCategory) {
      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);
    }
    
    for (var category in itemTypesByCategory) {
      requestCategories.push(
        <RequestCategory category={ category } paths={ paths } />
      )
    }
    return (
      <div id="request-container">
        <Switch>
          <Route exact path="/request/">
            <React.Fragment>
              <Row className='hero text-center'>
                <h2>
                  Choose an item you need
                </h2>
              </Row>
              { requestCategories }
            </React.Fragment>
          </Route>
          { routes }
        </Switch>
      </div>
    )
  }
};
