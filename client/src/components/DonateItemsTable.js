import React, { Component } from 'react';
import { Button, Table } from 'react-bootstrap';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Link, Route, Switch } from 'react-router-dom';


class DonateItemsTypeTable extends Component {
  render() {

    const { category, categoryPath, requests } = this.props;

    return (
      <Table>
        <thead>
          <tr>
            <th>Size</th>
            <th colSpan='2'>Location</th>
          </tr>
        </thead>
        <tbody>
          {
            requests ? requests.map((request) => {
              if (category === request.item.category_tag){
                return (
                  <tr key={request.id}>
                    <td>{ request.size }</td>
                    <td>{ request.city }</td>
                    <td><Button>Donate</Button></td>
                  </tr>
                )
              }
            }) : null
          }
        </tbody>
      </Table>
    )
  }
}


export default class DonateItemsTable extends Component {
  render() {

    const { requests, category, paths } = this.props;

    const visibleItems = {};

    const categoryItems = itemTypesByCategory[category];

    const categoryRequests = requests ? requests.filter((request) => {
      const itemType = request.item.tag;

      if (itemTypesByCategory[category].indexOf(itemType) > 0) {
        visibleItems[itemType] = true; // Only show items with requests
        return request;
      }
    }) : null

    const categoryPath = paths[category];

    if (categoryItems) {
      const itemsMap = categoryItems.map((categoryItem, index) => {

        const categoryItemPath = '/' + categoryPath + '/' + categoryItem + '/';

        return (
          <Route exact path={ categoryPath + '/:id' } key={ index }>
            <div>
              <DonateItemsTypeTable {...this.props } categoryRequests={ categoryRequests }  />
            </div>
          </Route>
        )
      })
      return (
        <Switch>
          {
            itemsMap
          }
        </Switch>
      )
    }
    else {
      return (
        <DonateItemsTypeTable {...this.props } categoryRequests={ categoryRequests }  />
      )
    }
  }
}
