import React, { Component } from 'react';
import { Col, Row, Button } from 'react-bootstrap';
import { Switch, Redirect, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../utils/constants';
import { withBreakpoints } from 'react-breakpoints';

import RequestForm from './RequestForm';
import RequestCategory from './RequestCategory';

export default withBreakpoints(class Request extends Component {
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
    const selectedCategories = [];

    const handleSelectItemType = (itemType) => {
      console.log(itemType)
      selectedCategories.push(itemType);
    }

    // Vary button text depending on width
    const { breakpoints, currentBreakpoint } = this.props;
    const confirmButtonText = (
      breakpoints[currentBreakpoint] >= breakpoints.tablet ? 'Confirm Request' : 'Confirm'
    );

    const renderItemTypeForCategory = (category) => (itemType) => {
      const path = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ path } key={ path }>
          <RequestForm itemType={ itemType } />
        </Route>
      );
    };

    for (var category in itemTypesByCategory) {
      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);
    }
    
    for (var category in itemTypesByCategory) {
      requestCategories.push(
        <RequestCategory category={ category } paths={ paths } handleSelectItemType= { handleSelectItemType }/>
      )
    }
    return (
      <div id="request-container">
        <Switch>
          <Route exact path="/request/">
            <React.Fragment>
              <Row className='hero text-center'>
                <h2>
                  Select up to 3 items you need.
                </h2>
              </Row>
                { requestCategories }
                <form onSubmit={ this.handleSubmit } className="col-sm-6 col-sm-offset-3">
                  <div className="text-center">
                    <Button type="submit" className="text-center">{ confirmButtonText }</Button>
                  </div>
              </form>
            </React.Fragment>
          </Route>
          { routes }
        </Switch>
      </div>
    )
  }
});
