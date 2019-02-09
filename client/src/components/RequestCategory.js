import React, { Component } from 'react';
import { Col, Row } from 'react-bootstrap';
import { itemTypesByCategory, itemInfo } from '../utils/constants';
import CategoryNav from './CategoryNav';
import Tile from './Tile';


class RequestItem extends Component {
  render() {
    const { itemType, category, handleSelectItemType } = this.props;
    const { displayName, icon } = this.props.info;

    return (
      <Col sm={3} xs={6}>
        <Tile
          side='request'
          displayName={ displayName }
          icon={ icon }
          category={ category }
          subcategory={ itemType }
          handleSelectItemType = { handleSelectItemType }
        />
      </Col>
    )
  }
}


class RequestItemsLinks extends Component {
  render() {
    const { category, handleSelectItemType } = this.props;

    const categoryItems = itemTypesByCategory[category];

    return (
      <Row>
        {
          categoryItems.map((item) => {
            return (<RequestItem 
                category={ category } 
                key={ item } 
                itemType={ item } 
                info={ itemInfo[item] } 
                handleSelectItemType = { handleSelectItemType }
              />)
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
        <Row>
          <h3>
            {this.props.category}
          </h3>
          <RequestItemsLinks { ...this.props } />
        </Row>
      </div>
    )
  }
}
