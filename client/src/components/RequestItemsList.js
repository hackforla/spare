import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Switch } from 'react-router-dom';
import Tile from './Tile';


class RequestItem extends Component {
  render() {
    const { displayName, icon } = this.props.info;
    // TODO: Put these styles in CSS/SASS
    return (
      <div className="col-sm-4 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>
        <div>
            <Tile side='request' alt={displayName} icon={icon} />
            <h1 className="text-center tile-label">#NEEDED</h1>
            <p className='text-label'>{displayName}</p>
        </div>
      </div>
    )
  }
}


class RequestItemsLinks extends Component {
  render() {
    const { category } = this.props;

    const categoryItems = itemTypesByCategory[category];

    return (
      <Row>
        {
          categoryItems.map((item) => {
            return (<RequestItem key={ item } info={ itemInfo[item] }/>)
          })
        }
      </Row>
    )
  }
}


export default class RequestItemsList extends Component {
  render() {
    return (
      <Switch>
        <RequestItemsLinks { ...this.props } />
      </Switch>
    )
  }
}
