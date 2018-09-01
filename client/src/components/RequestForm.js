import React, { Component } from 'react';
import axios from 'axios';

import { emailRegex, phoneRegex, itemInfo } from '../utils/constants';
import { Alert, Button, ControlLabel, FormControl, FormGroup, Row } from 'react-bootstrap';
import { withRouter } from "react-router-dom";
import { withBreakpoints } from 'react-breakpoints';
import MaskedInput from 'react-maskedinput';

import RequestConfirmation from './RequestConfirmation';

function getAllSizes(info) {
  const mens = info.sizeMen ? info.sizeMen.map(size => `Mens ${ size }`) : [];
  const womens = info.sizeWomen ? info.sizeWomen.map(size => `Womens ${ size }`) : [];

  if (mens || womens) {
    return mens.concat(womens);
  }
  else {
    return null;
  }
}

class RequestForm extends Component {
  constructor(props) {
    super(props);

    // Attach item info to component
    this.info = itemInfo[props.itemType];
    this.sizes = getAllSizes(this.info);

    this.state = {
      loading: true,
      neighborhoods: [],
      dirtyFields: [],

      // Field state values
      neighborhood: '',
      name: '',
      email: '',
      phone: '',
      size: this.sizes ? this.sizes[0] : ''
    }
  }

  handleInput = (event) => {
    const field = event.target.id;
    const value = event.target.value;

    // If user deletes from input, mark as dirty
    if (this.state[field] && value) {

      // Special case for phone (due to mask)
      if (field === 'phone') {
        if (this.state[field].replace(/\D/g,'').length > value.replace(/\D/g,'').length) {
          this.addDirtyField(field);
        }
      }
      else if (this.state[field].length > value.length) {
        this.addDirtyField(field);
      }
    }

    // Save input value to state
    this.setState({
      [field]: value
    });
  }

  handleSubmit = (event) => {
    event.preventDefault();

    // Process and clean data
    const {name, phone, email, size, neighborhood} = this.state;
    const data = {
      name, email, size, neighborhood
    }

    const phoneDigits = phone.replace(/\D/g,'');
    if (phoneDigits) {
      data['phone'] = '+1' + phoneDigits;
    }

    data['item'] = this.props.itemType;

    axios.post('/api/requests/', data)
      .then((res) => {
        this.setState({ submitSuccess: true });
      })
      .catch((err) => {
        // TODO: Handle case for 'too many requests'
        this.setState({ alert: 'danger', message: 'Request failed.' });
        console.error(err);
      });
  }

  addDirtyField = (field) => {
    const dirtyFields = [...this.state.dirtyFields];
    if (dirtyFields.indexOf(field) < 0) {
      dirtyFields.push(field);

      this.setState({
        dirtyFields
      });
    }
  }

  onBlur = (event) => {
    const field = event.target.id;
    this.addDirtyField(field);
  }

  componentDidMount() {
    axios.get('/api/neighborhoods/')
      .then((res) => {
        const defaultNeighborhood = res.data[0]

        this.setState({
          loading: false,
          neighborhoods: res.data,
          neighborhood: (defaultNeighborhood ? defaultNeighborhood.id : null)
        });
      })
      .catch((err) => {
        // TODO: Display error for user
        console.log(err)
      });
  }

  getValidationState(field) {
    const value = this.state[field];

    // Get early 'positive' validation for certain fields
    if (value) {
      switch(field) {
        case 'email':
          if (emailRegex.test(value)) {
            return 'success';
          }
          break;
        case 'phone':
          if (phoneRegex.test(value)) {
            return 'success';
          }
          break;
        default:
          // Do nothing
      }
    }

    // For other fields, don't try to validate unless user
    // has touched field
    if (this.state.dirtyFields.indexOf(field) < 0) {
      return null;
    }

    // Finally, return an validation result if field is dirty and
    // also invalid
    switch(field) {
      case 'neighborhood':
        return (value === undefined) ? 'error' : null;
      case 'name':
        return (value === '') ? 'error' : 'success';
      case 'email':
        return emailRegex.test(value) ? 'success' : 'error';
      case 'phone':
        // Optional field
        if (!value) {
          return null;
        }
        return phoneRegex.test(value) ? 'success': 'error';
      default:
        return null;
    }
  }

  getSizeOptions = () => {
    return this.sizes.map(size => <option key={size} value={size}>{ size }</option>);
  }

  getNeighborhoodOptions = () => {
    return this.state.neighborhoods.map(neighborhood => {
      return (<option key={neighborhood.id} value={neighborhood.id}>{neighborhood.name}</option>);
    });
  }

  render() {
    if (this.state.loading) {
      return null;
    }
    else if (this.state.submitSuccess) {
      return <RequestConfirmation />;
    }

    const neighborhoods = this.getNeighborhoodOptions();
    const sizeOptions = this.getSizeOptions();

    const pronoun = this.info.pluralPronoun ? 'those' : 'that'
    const headerMessage = `Cool, let's get you ${pronoun} ${this.info.verboseName}.`;

    // Vary button text depending on width
    const { breakpoints, currentBreakpoint } = this.props;
    const confirmButtonText = (
      breakpoints[currentBreakpoint] >= breakpoints.tablet ? 'Confirm Request' : 'Confirm'
    );

    return (
      <div>
        <div className="hero text-center">
          <h2>{ headerMessage }</h2>
          <p>
            We send your name and contact info to the person who wants to donate.
            <br />
            We don't post it on our site.
          </p>
        </div>
        <Row>
          <form onSubmit={ this.handleSubmit } className="col-sm-6 col-sm-offset-3">

            <FormGroup
              controlId="neighborhood"
              validationState={ this.getValidationState('neighborhood') }
              onBlur={ this.onBlur }
            >
              <ControlLabel>Nearest Neighborhood</ControlLabel>
              <FormControl
                componentClass="select"
                required
                value={ this.state.neighborhood }
                onChange={ this.handleInput }
              >
                { neighborhoods }
              </FormControl>
              <FormControl.Feedback />
            </FormGroup>

            <FormGroup
              controlId="name"
              validationState={ this.getValidationState('name') }
              onBlur={ this.onBlur }
            >
              <ControlLabel>Your First Name</ControlLabel>
              <FormControl
                type="text"
                placeholder={ 'Name' }
                required
                autoFocus={ true }
                value={ this.state.name }
                onChange={ this.handleInput }
              />
              <FormControl.Feedback />
            </FormGroup>

            <FormGroup
              controlId="email"
              validationState={ this.getValidationState('email') }
              onBlur={ this.onBlur }
            >
              <ControlLabel>Your Email</ControlLabel>
              <FormControl
                type="email"
                placeholder={ 'Email address' }
                required
                value={ this.state.email }
                onChange={ this.handleInput }
              />
              <FormControl.Feedback />
            </FormGroup>

            <FormGroup
              controlId="phone"
              validationState={ this.getValidationState('phone') }
              onBlur={ this.onBlur }
            >
              <ControlLabel>Your Phone Number</ControlLabel>
              <MaskedInput
                mask='(111) 111-1111'
                placeholder='Phone number'
                placeholderChar=' '
                id="phone"
                className="form-control"
                onChange={ this.handleInput }
              />
              <FormControl.Feedback />
            </FormGroup>

            {
              sizeOptions ?
              <FormGroup
                controlId="size"
                validationState={ this.getValidationState('size') }
                onBlur={ this.onBlur }
              >
                <ControlLabel>What Size?</ControlLabel>
                <FormControl
                  componentClass="select"
                  placeholder="select"
                  onChange={ this.handleInput }
                  value={ this.state.size }
                >
                  { sizeOptions }
                </FormControl>
              </FormGroup> : null
            }

            <div className="text-center">
              <Button type="submit" className="text-center">{ confirmButtonText }</Button>
            </div>
          </form>

        </Row>
      </div>
    )
  }
}


export default withRouter(withBreakpoints(RequestForm));
