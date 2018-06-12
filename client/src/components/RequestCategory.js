import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import { itemTypesByCategory, itemInfo } from '../constants';
import { Link } from 'react-router-dom';
import CategoryNav from './CategoryNav';
import Tile from './Tile';


class RequestItem extends Component {
  render() {
    const { itemType, category } = this.props;
    const { displayName, icon } = this.props.info;
    // TODO: Put these styles in CSS/SASS
    return (
      <div className="col-sm-3 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>
        <Link to={ '/request/' + category + '/' + itemType + '/' }>
          <Tile side='request' alt={displayName} icon={icon} />
          <p className='text-label'>{displayName}</p>
        </Link>
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
            return (<RequestItem category={ category } key={ item } itemType={ item } info={ itemInfo[item] }/>)
          })
        }
      </Row>
    )
  }
}


export default class RequestItemsList extends Component {
  render() {
    const { paths } = this.props;

    return (
      <div>
        <Row className='text-center'>
          <h2>
            Choose an item you need
          </h2>
        </Row>
        <Row>
          <CategoryNav paths={ paths } />
          <RequestItemsLinks { ...this.props } />
        </Row>
      </div>
    )
  }
}
