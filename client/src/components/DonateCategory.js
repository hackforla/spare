import React, { Component } from 'react';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Col, Row } from 'react-bootstrap';
import CategoryNav from './CategoryNav';
import Tile from './Tile';


class DonateSubcategoryLink extends Component {
  render() {
    const { count, category, subcategory } = this.props;
    const { displayName, icon } = this.props.info;

    const neededText = `${ count } requests`;

    return (
      <Col sm={3} xs={12}>
        <Tile
          side='donate'
          displayName={displayName}
          icon={ icon }
          hoverText={ neededText }
          category={ category }
          subcategory={ subcategory }
        />
      </Col>
    )
  }
}


export default class DonateCategory extends Component {
  getRequestsByType(requests) {
    const { category } = this.props;

    const results = {};

    if (!requests) {
      return null;
    }
    else {
      // Initialize empty list for each item type
      itemTypesByCategory[category].forEach((itemType) => {
        results[itemType] = [];
      });

      //  Add request to each list
      requests.forEach((itemRequest) => {
        const itemType = itemRequest.item.tag;
        if (itemRequest.item.category_tag === category) {
          results[itemType].push(itemRequest);
        }
      });

      return results;
    }
  }

  render() {
    const { requests, category, paths } = this.props;

    const requestsByItemType = this.getRequestsByType(requests);

    let items = [];

    // Value is only null when there are no requests
    if (requestsByItemType !== null) {
      for (var index in itemTypesByCategory[category]) {
        const itemType = itemTypesByCategory[category][index];
        const itemTypeRequests = requestsByItemType[itemType];

        if (itemTypeRequests.length > 0) {
          items.push(
            <DonateSubcategoryLink
              { ...this.props }
              count={ itemTypeRequests.length }
              info={ itemInfo[itemType] }
              key={ index }
              subcategory={ itemType }
            />
          );
        }
      }
    }

    if (items.length < 1) {
      items.push(
        <div key={ 0 }>
          <p>There are not requests for this item right now. Please check back later!</p>
        </div>
      )
    }

    return (
      <div>
        <Row className='hero text-center'>
          <h2>
            Give spare items directly to people in need.
            <br />
            What could you spare?
          </h2>
        </Row>
        <Row>
          <CategoryNav paths={ paths  } />
          { requests !== null ? items : [] }
        </Row>
      </div>
    )
  }
}
