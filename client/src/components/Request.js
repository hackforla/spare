import axios from 'axios';
import React, { Component } from 'react';
import { Button, Row } from 'react-bootstrap';
import ItemsList from './ItemsList';
import { LinkContainer } from 'react-router-bootstrap';
import { Switch, Redirect, Route } from 'react-router-dom';
import CategoryNav from './CategoryNav';


export default class Request extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    axios.get('http://localhost:8000/api/requests/')
      .then((res) => {
        this.setState((oldState) => ({
          requests: res.data
        }));
      })
      .catch((err) => {
        this.setState((oldState) => ({alert: 'danger', message: 'Unable to get donation data. Please try again later.'}));
        console.log(err)
      });
  }

  render() {
    const { mode, match } = this.props;
    const { requests } = this.state;

    const paths = {
      'clothing': match.path + '/clothing',
      'essentials': match.path + '/essentials',
      'hygiene': match.path + '/hygiene',
      'donate': '/donate',
      'request': '/request',
    };

    let switchModeButton;
    if (mode === 'donate') {
      switchModeButton = (
        <LinkContainer to={ paths.request }>
          <Button>Request an item</Button>
        </LinkContainer>
      )
    }
    else if (mode === 'request') {
      switchModeButton = (
        <LinkContainer to={ paths.donate }>
          <Button>Donate an item</Button>
        </LinkContainer>
      )
    }

    return (
      <div>
        { switchModeButton }
        <Row className='text-center'>
          <h2>
            Choose an item you need
          </h2>
        </Row>
        <Row>
          <CategoryNav mode={ mode } match={ match } paths={ paths } />
        </Row>
        <Switch>
          <Route exact path={ paths.clothing }>
            <ItemsList mode={ mode } category='clothing' requests={ requests } paths={ paths } />
          </Route>
          <Route exact path={ paths.essentials }>
            <ItemsList mode={ mode } category='essentials' requests={ requests } paths={ paths } />
          </Route>
          <Route exact path={ paths.hygiene }>
            <ItemsList mode={ mode } category='hygiene' requests={ requests } paths={ paths } />
          </Route>
          <Redirect exact from={ match.path } to={ paths.clothing }/>
        </Switch>
      </div>
    )
  }
};
