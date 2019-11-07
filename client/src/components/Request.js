import React, { Component } from 'react';
import { Row } from 'react-bootstrap';
import { Switch, Route } from 'react-router-dom';
import { itemTypesByCategory } from '../utils/constants';

import RequestForm from './RequestForm';
import RequestCategory from './RequestCategory';
import RequestModal from './RequestModal';


export default class Request extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modalIsOpen: false,
    }

    this.openModal = this.openModal.bind(this);
    this.closeModal = this.closeModal.bind(this);
  }

  openModal() {
    this.setState({modalIsOpen: true});
  }

  closeModal() {
    this.setState({modalIsOpen: false});
  }

  render() {
    const { match } = this.props;

    const paths = {
    'clothing': match.path + '/clothing',
      'essentials': match.path + '/essentials',
      'hygiene': match.path + '/hygiene',
      'donate': '/donate',
      'request': '/request',
    };

    const routes = [];
    const requestCategories = [];

    const renderItemTypeForCategory = (category) => (itemType) => {
      const path = paths[category] + '/' + itemType + '/';
      routes.push(
        <Route exact path={ path } key={ path }>
          <RequestForm itemType={ itemType }/>
        </Route>
      );
    };

    var category;

    for (category in itemTypesByCategory) {
      const renderItemType = renderItemTypeForCategory(category);
      itemTypesByCategory[category].forEach(renderItemType);
    }

    for (category in itemTypesByCategory) {
      requestCategories.push(
        <RequestCategory category={ category } paths={ paths } openModal={ this.openModal }/>
      )
    }

    const modalStyle = {
      overlay: {
        backgroundColor: 'rgba(0, 0, 0, 0.25)'
      },
      content : {
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '60%',
        border: '1px solid #ccc',
        borderRadius: '2px'
      }
    }

    return (
      <div id="request-container">
        <Switch>
          <Route exact path="/request/">
            <React.Fragment>
              <Row className='hero text-center'>
                <h2>
                  Choose an item you need
                </h2>
              </Row>
              { requestCategories }
            </React.Fragment>
          </Route>
          { routes }
        </Switch>
        <RequestModal
          style={ modalStyle }
          isOpen={ this.state.modalIsOpen }
          onRequestClose={ this.closeModal }
        />
      </div>
    )
  }
};
