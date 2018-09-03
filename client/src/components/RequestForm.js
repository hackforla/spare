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
      validationStates: {},

      // Field state values
      neighborhood: '',
      name: '',
      email: '',
      phone: '',
      size: this.sizes ? this.sizes[0] : ''
    }
  }

  fields = {
    neighborhood: {
      isRequired: true,
    },
    name: {
      isRequired: true,
      validator: (value) => {
        if (value === '') {
          return 'Field is required'
        }
      }
    },
    email: {
      isRequired: false,
      earlyPositive: true,
      validator: (value) => {
        if (!emailRegex.test(value)) {
          return 'Please enter a valid email'
        }
      },
    },
    phone: {
      isRequired: false,
      earlyPositive: true,
      validator: (value) => {
        if (!phoneRegex.test(value)) {
          return 'Please enter a valid phone number'
        }
      },
      clean: (value) => { return value.replace(/\D/g,''); },
    },
    size: {
      isRequired: true,
    }
  }

  validateField = (fieldName, value) => {
    const field = this.fields[fieldName];

    // If not required, return null
    if (!field.isRequired && (value === '')) {
      return { status: null };
    }

    // Otherwise, return validation result
    const validator = field.validator;
    if (validator) {
      const error = validator(value);
      if (error) {
        return { status: 'error', msg: error };
      }
      else {
        return { status: 'success' };
      }
    }

    return { status: null };
  }

  isDirty = (fieldName) => {
    return (this.state.dirtyFields.indexOf(fieldName) >= 0);
  }

  handleInput = (event) => {
    const fieldName = event.target.id;
    const value = event.target.value;
    const currValue = this.state[fieldName];
    const field = this.fields[fieldName];

    let fieldDirty = this.isDirty(fieldName);

    // If user deletes from input, mark as dirty
    if (currValue && value) {
      const noop = (value) => { return value};
      const clean = field.clean ? field.clean : noop;

      if (clean(currValue).length > clean(value).length) {
        this.addDirtyField(fieldName);

        // Keep track locally of whether field is now dirty
        fieldDirty = true;
      }
    }

    const validationResult = this.validateField(fieldName, value);
    if (fieldDirty || ((validationResult.status === 'success') && field.earlyPositive)) {
      const validationStates = this.state.validationStates;
      validationStates[fieldName] = validationResult
      this.setState({
        validationStates
      });
    }

    // Save input value
    this.setState({
      [fieldName]: value
    });
  }

  getSerializedData = () => {
    // Process and clean data
    const {name, phone, email, size, neighborhood} = this.state;
    const data = {
      name, email, size, neighborhood
    }

    const phoneDigits = this.fields.phone.clean(phone);
    if (phoneDigits) {
      data['phone'] = '+1' + phoneDigits;
    }

    data['item'] = this.props.itemType;
    return data;
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const data = this.getSerializedData();

    axios.post('/api/requests/', data)
      .then((res) => {
        this.setState({ submitSuccess: true });
      })
      .catch((err) => {
        switch (err.response.status) {
          case 400:
            // Serializer/validation errors
            const errors = err.response.data
            if (errors['non_field_errors']) {
              this.setState({
                alert: {
                  level: 'danger',
                  message: (<div>
                    <p>
                      { errors['non_field_errors'] }
                    </p>
                  </div>)
                }
              });
            }

            const validationStates = this.state.validationStates;
            for (let field in this.fields) {
              if (err.response.data[field]) {
                validationStates[field] = {
                  status: 'error',
                  msg: err.response.data[field][0]
                }
              }
            }
            this.setState({
              validationStates
            })
            break;
          // User is being throttled
          case 429:
            this.setState({
              alert: {
                level: 'danger',
                message: (<div>
                  <p>
                    <strong>Request limit reached</strong><br />
                    Looks like you've reached the request limit! :(<br />
                    Please try again in 24 hours
                  </p>
                </div>)
              }
            });
            break;
          // All other errors
          default:
            this.setState({
              alert: {
                level: 'danger',
                message: (<div>
                  <p>
                    <strong>Problem submitting request</strong><br />
                    Please contact us if problems persist.<br />
                  </p>
                </div>)
              }
            });
        }
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
    // When field is blurred/deselected, mark as 'dirty'
    const fieldName = event.target.id;
    this.addDirtyField(fieldName);

    const validationResult = this.validateField(fieldName, this.state[fieldName]);
    const validationStates = this.state.validationStates;
    validationStates[fieldName] = validationResult
    this.setState({
      validationStates
    });
  }

  componentDidMount() {
    // Populate neighborhood select field
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

  getNeighborhoodOptions = () => {
    // Return neighborhood options for select
    return this.state.neighborhoods.map(neighborhood => {
      return (<option key={neighborhood.id} value={neighborhood.id}>{neighborhood.name}</option>);
    });
  }

  getSizeOptions = () => {
    // Return size options for select
    return this.sizes.map(size => <option key={size} value={size}>{ size }</option>);
  }

  dismissAlert = () => {
    this.setState({
      alert: null,
    });
  }

  getError = (fieldName) => {
    const validationState = this.state.validationStates[fieldName];
    if (validationState && (validationState.status === 'error')) {
      return <div className="help-block">{ validationState.msg }</div>;
    }
    else {
      return <div className="help-block"></div>;
    }
  }

  // Not currently used, but could be used to disable submit button
  hasErrors = () => {
    for (let field in this.fields) {
      const validationState = this.state.validationStates[field];
      if (validationState && (validationState.status === 'error')) {
        return true;
      }

      // We also need to actually validate fields (in case not dirty yet)
      const validationResult = this.validateField(field, this.state[field]);
      if (validationResult.status === 'error') {
        return true;
      }
    }

    return false;
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
    const validationStates = this.state.validationStates;

    const pronoun = this.info.pluralPronoun ? 'those' : 'that'
    const headerMessage = `Cool, let's get you ${pronoun} ${this.info.verboseName}.`;

    // Vary button text depending on width
    const { breakpoints, currentBreakpoint } = this.props;
    const confirmButtonText = (
      breakpoints[currentBreakpoint] >= breakpoints.tablet ? 'Confirm Request' : 'Confirm'
    );

    const alert = this.state.alert;
    const formAlert = (
      alert && alert.message ?
      <Alert bsStyle={ alert.level } onDismiss={ this.dismissAlert } >
        { alert.message }
      </Alert> : null
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
              validationState={ validationStates.neighborhood && validationStates.neighborhood.status }
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
              validationState={ validationStates.name && validationStates.name.status }
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
              { this.getError('name') }
            </FormGroup>

            <FormGroup
              controlId="email"
              validationState={ validationStates.email && validationStates.email.status }
              onBlur={ this.onBlur }
            >
              <ControlLabel>Your Email</ControlLabel>
              <FormControl
                type="email"
                placeholder={ 'Email address' }
                value={ this.state.email }
                onChange={ this.handleInput }
              />
              <FormControl.Feedback />
              { this.getError('email') }
            </FormGroup>

            <FormGroup
              controlId="phone"
              validationState={ validationStates.phone && validationStates.phone.status }
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
              { this.getError('phone') }
            </FormGroup>

            {
              sizeOptions && sizeOptions.length ?
              <FormGroup
                controlId="size"
                validationState={ validationStates.size && validationStates.size.status }
                onBlur={ this.onBlur }
              >
                <ControlLabel>What Size?</ControlLabel>
                <FormControl
                  componentClass="select"
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
            { formAlert }
          </form>
        </Row>
      </div>
    )
  }
}


export default withRouter(withBreakpoints(RequestForm));
