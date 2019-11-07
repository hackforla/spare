import React, { Component } from 'react';
import { Button, Table, Row } from 'react-bootstrap';
import { withBreakpoints } from 'react-breakpoints';
import { itemTypesByCategory, itemInfo } from '../utils/constants';
import { Route, Switch } from 'react-router-dom';
import { LinkContainer } from 'react-router-bootstrap';


class DonateItemsTypeTableSmall extends Component {
  render() {

    const { category, requestsForSubcategory, subcategory } = this.props;

    return (
      <div>
        {
          requestsForSubcategory ? requestsForSubcategory.map((request) => {
            if (subcategory.slug === request.type.slug){
              return (
                <Table responsive className='table-requests-mobile' key={request.id}>
                  <tbody key={request.id}>
                    <tr>
                      <td>
                        <span className="table-requests-mobile-header">Size</span><br />
                        { request.size || 'N/A' }
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <span className="table-requests-mobile-header">Location</span><br />
                        { request.neighborhood.name }
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <LinkContainer to={`/donate/${ category.tag }/${ request.item.category_tag }/${ request.id }`}>
                          <Button>Donate</Button>
                        </LinkContainer>
                      </td>
                    </tr>
                  </tbody>
                </Table>
              )
            }
            else {
              return null;
            }
          }) : null
        }
      </div>
    )
  }
}


class DonateItemsTypeTableLarge extends Component {
  render() {

    const { category, subcategory, requestsForSubcategory } = this.props;

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
            requestsForSubcategory ? requestsForSubcategory.map((request) => {
              if (subcategory.slug === request.type.slug){
                return (
                  <tr key={request.id}>
                    <td className="col-md-5">{ request.size || 'N/A' }</td>
                    <td className="col-md-4">{ request.neighborhood.name }</td>
                    <td className="col-md-3 text-right">
                      <LinkContainer to={`/donate/${ category.slug }/${ request.type.slug }/${ request.id }`}>
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

          requestItem = {...requestItem, ...request};

          results[slug].push(requestItem);
        });
      });

    }

    return results;
  }

  render() {
    const { breakpoints, currentBreakpoint, category, subcategory, requests } = this.props;

    const requestsByItemType = this.getRequestsByType(requests);
    let requestsForSubcategory = [];
    if (requestsByItemType !== null) {
      requestsForSubcategory = requestsByItemType[subcategory.slug];
    }

    let itemsTable = null;
    if (breakpoints[currentBreakpoint] >= breakpoints.tablet) {
      itemsTable = (
        <DonateItemsTypeTableLarge requests={requests} category={category} subcategory={subcategory} requestsForSubcategory={requestsForSubcategory} />
      )
    }
    else {
      itemsTable = (
        <DonateItemsTypeTableSmall requests={requests} category={category} subcategory={subcategory} requestsForSubcategory={requestsForSubcategory} />
      )
    }

    return (
      <div>
        <Row className="hero text-center">
          <h2>Here are all of the requests for { subcategory.inline_text_name }</h2>
        </Row>
        { itemsTable }
      </div>
    )
  }
}


class DonateItemsTable extends Component {
  render() {
    const { category, paths, requests } = this.props;
    const items = [];

    category.subcategories.forEach((subcategory) => {
      const path = paths[category.slug] + '/' + subcategory.slug + '/';

      items.push(
        <Route exact path={ path } key={ subcategory.slug }>
          <DonateItemsTypeTable { ...this.props } />
        </Route>
      );
    });


    return (
      <Switch>
        {
          items
        }
      </Switch>
    )
  }
}


export default withBreakpoints(DonateItemsTable);
