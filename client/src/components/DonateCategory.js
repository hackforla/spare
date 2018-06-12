import React, { Component } from 'react';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import CategoryNav from './CategoryNav';
import Tile from './Tile';


class DonateSubcategoryLink extends Component {
  render() {
    const { category, subcategory } = this.props;
    const { displayName, icon } = this.props.info;

    // TODO: Put these styles in CSS/SASS
    return (
      <div className="col-sm-4 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>
        <div>
          <Tile side='donate' alt={displayName} icon={ icon } />
          <p className='text-label'>
            <Link to={ '/donate/' + category + '/' + subcategory + '/' } >{ displayName }</Link>
          </p>
        </div>
      </div>
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
            <DonateSubcategoryLink { ...this.props } info={ itemInfo[itemType] } key={ index } subcategory={ itemType } />
          );
        }
      }
    }

    return (
      <div>
        <Row className='text-center'>
          <h2>
            Give spare items directly to people in need.
            <br />
            What could you spare?
          </h2>
        </Row>
        <Row>
          <CategoryNav paths={ paths  } />
          { items }
        </Row>
      </div>
    )
  }
}
