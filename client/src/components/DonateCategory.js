import React, { Component } from 'react';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Row } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import CategoryNav from './CategoryNav';
import Tile from './Tile';


class DonateSubcategoryLink extends Component {
  render() {
    const { requests, category, subcategory } = this.props;
    const { displayName, icon } = this.props.info;

    if (requests.length < 1) {
      return null;
    }
    else {
      // TODO: Put these styles in CSS/SASS
      return (
        <div className="col-sm-3 col-xs-12" style={{
          minWidth: '150px',
          minHeight: '150px',
        }}>
          <Link to={ '/donate/' + category + '/' + subcategory + '/' } >
            <Tile side='donate' alt={displayName} icon={ icon } />
            <span className="text-center tile-label">{ requests.length } needed</span>
            <div className='text-label'>{ displayName }</div>
          </Link>
        </div>
      )
    }
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

        items.push(
          <DonateSubcategoryLink { ...this.props } requests={ itemTypeRequests } info={ itemInfo[itemType] } key={ index } subcategory={ itemType } />
        );
      }
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
          { items }
        </Row>
      </div>
    )
  }
}
