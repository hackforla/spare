import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import { itemsByCategory, itemInfo } from '../constants';


class RequestItem extends Component {
  render() {
    const { displayName } = this.props.info;
    // TODO: Put these styles in CSS/SASS
    return (
      <div class="col-sm-4 col-xs-12" style={{
        minWidth: '150px',
        minHeight: '150px',
      }}>{ displayName }</div>
    )
  }
}


export default class RequestItemsList extends Component {
  render() {
    const { category } = this.props;

    const categoryItems = itemsByCategory[category];

    return (
      <Row>
        {
          categoryItems.map(function(item){
            return (<RequestItem key={ item } info={ itemInfo[item] }/>)
          })
        }
      </Row>
    )
  }
}
