import React, { Component } from 'react';
import { Button, Table, Row } from 'react-bootstrap';
import { Media } from 'react-breakpoints';
import { itemTypesByCategory } from '../constants';
import { Route, Switch } from 'react-router-dom';
import { LinkContainer } from 'react-router-bootstrap';
import { itemInfo } from '../constants';


class DonateItemsTypeTableSmall extends Component {
  render() {

    const { category, requestsForItemType } = this.props;

    return (
      <Table responsive>
        {
          requestsForItemType ? requestsForItemType.map((request) => {
            if (category === request.item.category_tag){
              return (
                <tbody key={request.id}>
                  <tr>
                    <th>Size:</th>
                    <td>{ request.size || 'N/A' }</td>
                  </tr>
                  <tr>
                    <th>Location:</th>
                    <td>{ request.neighborhood.name }</td>
                  </tr>
                  <tr>
                    <td colSpan="2">
                      <LinkContainer to={`/donate/${ request.id }`}>
                        <Button>Donate</Button>
                      </LinkContainer>
                    </td>
                  </tr>
                </tbody>
              )
            }
            else {
              return null;
            }
          }) : null
        }
      </Table>
    )
  }
}


class DonateItemsTypeTableLarge extends Component {
  render() {

    const { category, requestsForItemType } = this.props;

    return (
      <Table responsive>
        <thead>
          <tr>
            <th className="col-md-5">Size</th>
            <th colSpan='2' className="col-md-7">Location</th>
          </tr>
        </thead>
        <tbody>
          {
            requestsForItemType ? requestsForItemType.map((request) => {
              if (category === request.item.category_tag){
                return (
                  <tr key={request.id}>
                    <td className="col-md-5">{ request.size || 'N/A' }</td>
                    <td className="col-md-4">{ request.neighborhood.name }</td>
                    <td className="col-md-3 text-right">
                      <LinkContainer to={`/donate/${ request.id }`}>
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
      <div>
        <Row className="hero text-center">
          <h2>Here are all of the requests for { itemInfo[itemType].verboseName }</h2>
        </Row>
        <Media>
          {({breakpoints, currentBreakpoint}) => {
            switch (currentBreakpoint) {
              case 'mobile':
              case 'mobileLandscape':
              case 'tablet':
                return <DonateItemsTypeTableSmall requests={requests} category={category} requestsForItemType={requestsForItemType} />
              default:
                return <DonateItemsTypeTableLarge requests={requests} category={category} requestsForItemType={requestsForItemType} />
            }
          }}
        </Media>
      </div>
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
          <DonateItemsTypeTable { ...this.props } />
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
