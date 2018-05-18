import React, { Component } from 'react';
import { Button, Table } from 'react-bootstrap';
import { itemTypesByCategory } from '../constants';
import { Route, Switch } from 'react-router-dom';


class DonateItemsTypeTable extends Component {
  render() {

    const { category, requests } = this.props;

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
