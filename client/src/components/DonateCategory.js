import React, { Component } from 'react';
import { itemTypesByCategory, itemInfo } from '../utils/constants';
import { Col, Row } from 'react-bootstrap';
import Tile from './Tile';


class DonateSubcategoryLink extends Component {
  render() {
    const { disabled, count, category, subcategory } = this.props;
    const { displayName, icon } = this.props.info;

    const neededText = (count === 1) ? `${ count } request` : `${ count } requests`;

    return (
      <Col sm={3} xs={6}>
        <Tile
          disabled={disabled}
          side='donate'
          displayName={displayName}
          icon={ icon }
          hoverText={ neededText }
          category={ category.slug }
          subcategory={ subcategory.slug }
        />
      </Col>
    )
  }
}

export default class DonateCategory extends Component {
  getRequestsByType(requests) {
    const results = {};

    if (!requests) {
      return null;
    }
    else {
      //  Add request to each list
      requests.forEach((request) => {
        request.request_items.forEach((requestItem) => {
          const slug = requestItem.type.slug;

          if (results[slug] == null) {
            results[slug] = [];
          }

          results[slug].push(requestItem);
        });
      });

    }

    return results;
  }


  render() {
    const { requests, category, subcategories } = this.props;

    const requestsByItemType = this.getRequestsByType(requests);

    let items = [];

    // Value is only null when there are no requests
    if (requestsByItemType !== null && subcategories) {
      subcategories.forEach((subcategory) => {
        const subcategoryRequests = requestsByItemType[subcategory.slug];

        if (subcategoryRequests && (subcategoryRequests.length > 0)) {
          items.push(
            <DonateSubcategoryLink
              { ...this.props }
              count={ subcategoryRequests.length }
              info={ itemInfo[subcategory.slug] }
              key={ subcategory.slug }
              subcategory={ subcategory }
            />
          );
        }
      });
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
        <Row>
          <h3>
            {this.props.category.display_name}
          </h3>
          { requests !== null ? items : [] }
        </Row>
      </div>
    )
  }
}
