import React, { Component } from 'react';
import { itemTypesByCategory, itemInfo } from '../constants';
import DonateItemsTable from './DonateItemsTable';
import { Link } from 'react-router-dom';


class DonateItem extends Component {
  render() {
    const { category, tag } = this.props;
    const { displayName } = this.props.info;
    // TODO: Put these styles in CSS/SASS
    return (
      <div className="col-sm-4 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>
        <Link to={ '/donate/' + category + '/' + tag } >{ displayName }</Link>
      </div>
    )
  }
}


class DonateItemsLinks extends Component {
  render() {
    const { requests, category } = this.props;

    const requestsByItemType = {};

    const categoryRequests = requests ? requests.filter((request) => {
      const categoryItems = itemTypesByCategory[category];
      const itemType = request.item.tag;

      if (categoryItems.indexOf(itemType) > 0) {
        if (!(itemType in requestsByItemType)) {
          requestsByItemType[itemType] = [];
        }

        requestsByItemType[itemType].push(request);
        return request;
      }
      else {
        return null;
      }
    }) : [];

    if (categoryRequests.length) {
      const visibleItems = [];

      for (var itemType in requestsByItemType){
        visibleItems.push(itemType);
      }
      return visibleItems.map((item) => {
        return <DonateItem key={ item } category={ category } tag={ item } info={ itemInfo[item] } />;
      });
    }
    else {
      return (
        <p>No current requests for this item. Please check back later!</p>
      )
    }
  }
}


export default class DonateItemsList extends Component {
  render() {
    return (
      <div>
        <DonateItemsTable {...this.props} />
      </div>
    )
  }
}
