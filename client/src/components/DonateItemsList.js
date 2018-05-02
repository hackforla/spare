import React, { Component } from 'react';
import { Button, Table } from 'react-bootstrap';


export default class DonateItemsList extends Component {
  render() {
    const { requests, category } = this.props;

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
            requests ? requests.map(function(request){
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
