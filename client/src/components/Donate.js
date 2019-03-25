import axios from 'axios';
import React, { Component } from 'react';
import { Col, Row } from 'react-bootstrap';
import { Link, Switch, Route } from 'react-router-dom';
import { itemTypesByCategory, itemInfo } from '../utils/constants';
import DonateCategory from './DonateCategory';
import DonateItemsTable from './DonateItemsTable';
import FulfillmentForm from './FulfillmentForm';
import Tile from './Tile';

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

  /*
   * When there are no donation requests, just show the clothing icons.
   */
  renderNoRequests() {
    const category = 'clothing';
    const clothingTiles = itemTypesByCategory[category];

    const renderTile = (itemType, index) => {
      const { displayName, icon } = itemInfo[itemType];
      return (
        <Col sm={3} xs={6} key={ index }>
          <Tile
            disabled
            side='donate'
            displayName={displayName}
            icon={ icon }
            hoverText={ '0 requests' }
            category={ category }
            subcategory={ itemType }
          />
        </Col>
      )
    };
      
    return (
      <React.Fragment>
        <div id="no-items">
          <Row className="background">
            {clothingTiles.slice(0, 4).map(renderTile)}
          </Row>
          <Row>
            <p className="col-sm-12 col-xs-12">
              <span className="intro">There are no needs right now</span>
              <Link to="/request">Ask for an item</Link>
            </p>
          </Row>
          <Row className="background">
            {clothingTiles.slice(4).map(renderTile)}
          </Row>
        </div>
      </React.Fragment>
    );
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
    let donateCategories = [];

    const renderItemTypeForCategory = (category) => (itemType) => {
      const itemTypePath = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ itemTypePath } key={ itemTypePath }>
          <DonateItemsTable itemType={ itemType } category={ category } requests={ requests } paths={ paths } />
        </Route>
      );
    };

    const requestPath = "/donate/:category/:item/:id";

    routes.push(
      <Route exact path={ requestPath } key={ requestPath } render={ props => <DonationDetail {...props} requests={ requests } /> } />
    );

    for (var category in itemTypesByCategory) {
      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);

      donateCategories.push(
        <DonateCategory category={ category } requests={ requests } paths={ paths } />
      );
    }

    return (
      <div id="donate-container">
        <Switch>
          <Route exact path="/donate/">
            <React.Fragment>
              <Row className='hero text-center'>
                <h2>
                  Select the gently used or new items you can give to those in need.
                </h2>
                <p>All hygiene items must be new.</p>
              </Row>
              { (Array.isArray(requests) && requests.length === 0) ? this.renderNoRequests() : donateCategories }
            </React.Fragment>
          </Route>
          { routes }
        </Switch>
      </div>
    )
  }
};
