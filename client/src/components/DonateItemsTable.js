import React, { Component } from 'react';
import { Button, Table } from 'react-bootstrap';
import { itemTypesByCategory } from '../constants';
import { Route, Switch } from 'react-router-dom';
import { LinkContainer } from 'react-router-bootstrap';


class DonateItemsTypeTable extends Component {
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
    const { category, itemType, requests } = this.props;

    const requestsByItemType = this.getRequestsByType(requests);
    let requestsForItemType = [];
    if (requestsByItemType !== null) {
      requestsForItemType = requestsByItemType[itemType];
    }

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
            requestsForItemType ? requestsForItemType.map((request) => {
              if (category === request.item.category_tag){
                return (
                  <tr key={request.id}>
                    <td>{ request.size }</td>
                    <td>{ request.city }</td>
                    <td>
                      <LinkContainer to={'/specific/page'}>
                        <Button>Donate</Button>
                      </LinkContainer>
                    </td>
                  </tr>
                )
              }
              else {
                return null;
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

    const { category, paths } = this.props;

    let items = [];
    for (var item in itemTypesByCategory[category]) {
      const itemType = itemTypesByCategory[category][item]
      items.push(
        <Route exact path={ paths[category] + '/' + itemType + '/' } key={ item }>
          <h2>
            <DonateItemsTypeTable { ...this.props } />
          </h2>
        </Route>
      );
    }


    return (
      <Switch>
        {
          items
        }
      </Switch>
    )
  }
}
