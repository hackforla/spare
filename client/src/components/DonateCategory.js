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
          <h1 className="text-center tile-label">#NEEDED</h1>
          <Link to={ '/donate/' + category + '/' + subcategory + '/' } >{ displayName }</Link>
        </div>
      </div>
    )
  }
}


export default class DonateCategory extends Component {
  getCategoryRequests(requests) {
    const { category } = this.props;

    if (!requests) {
      return null;
    }
    else {
      const results = {};

      requests.filter((itemRequests) => {
        return (
          (itemRequests.category === category) && (itemRequests.count)
        );
      }).forEach((itemRequests) => {
        results[itemRequests.type] = itemRequests.count;
      });

      return results;
    }
  }

  render() {
    const { requests, category, paths } = this.props;

    const categoryRequests = this.getCategoryRequests(requests);

    let items;

    // Value is only null when there are no requests
    if (categoryRequests !== null) {
      if (Object.keys(categoryRequests).length !== 0) {
        items = [];

        for (var item in itemTypesByCategory[category]) {
          const subcategory = itemTypesByCategory[category][item];
          if (categoryRequests[subcategory]) {
            items.push(
                <DonateSubcategoryLink { ...this.props } info={ itemInfo[subcategory] } key={ item } subcategory={ subcategory } />
            );
          }
        }
      }
      else {
        items = (
          <p>No current requests for this category. Please check back later!</p>
        );
      }
    }
    else if(categoryRequests !== null) {
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
