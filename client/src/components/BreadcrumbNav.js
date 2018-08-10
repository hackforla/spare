import React, { Component } from 'react';
import { Breadcrumb } from 'react-bootstrap';
import { Route, Switch } from "react-router-dom";
import { itemInfo } from '../utils/constants';


class CategoryBreadcrumb extends Component {
  render() {
    const {mode, item} = this.props.match.params;

    const modeName = mode === 'request' ? 'Request' : 'Donate';

    const info = itemInfo[item];

    if (!info) {
      return null;
    }
    else {
      return (
        <Breadcrumb className={ `${ mode }-text` }>
          <Breadcrumb.Item href={`/${ mode }`}>{ modeName }</Breadcrumb.Item>
          <Breadcrumb.Item active>{ info.displayName }</Breadcrumb.Item>
        </Breadcrumb>
      )
    }
  }
}



class DetailBreadcrumb extends Component {
  render() {
    const {mode, category, item} = this.props.match.params;

    const modeName = mode === 'request' ? 'Request' : 'Donate';

    const info = itemInfo[item];

    if (!info) {
      return null;
    }
    else {
      return (
        <Breadcrumb className={ `${ mode }-text` }>
          <Breadcrumb.Item href={`/${ mode }`}>{ modeName }</Breadcrumb.Item>
          <Breadcrumb.Item href={`/${ mode }/${ category }/${ item }`}>{ info.displayName }</Breadcrumb.Item>
          <Breadcrumb.Item active>Detail</Breadcrumb.Item>
        </Breadcrumb>
      )
    }
  }
}


export default class BreadcrumbNav extends Component {
  render() {
    return (
      <div>
        <Switch>
          <Route
            exact path='/:mode/:category/:item/:id/'
            component={ DetailBreadcrumb }
          />
          <Route
            exact path='/:mode/:category/:item/'
            component={ CategoryBreadcrumb }
          />
        </Switch>
      </div>
    )
  }
}
