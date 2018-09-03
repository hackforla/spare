import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import { emailRegex, phoneRegex, itemInfo } from '../utils/constants';
import FulfillmentConfirmation from './FulfillmentConfirmation';
import { Alert, Button, ControlLabel, FormControl, FormGroup, Radio, Row } from 'react-bootstrap';
import { withBreakpoints } from 'react-breakpoints';
import MaskedInput from 'react-maskedinput';

const now = moment();

// expects time to be a string formatted as HH:MM:SS
const formatTime = (time) => {
  const split = time.split(':');
  const formatted = now
    .hours(split[0])
    .minutes(split[1])
    .seconds(split[2])
    .format('h:mm A');
  return formatted;
};

class FulfillmentForm extends Component {
  constructor(props) {
    super(props);

    // Attach item info to component
    this.info = itemInfo[props.request.item.tag];
    this.sizes = {};

    this.state = {
      loading: true,
      dropoffTimes: [],
      dirtyFields: [],
      validationStates: {},

      // Field state values
      name: '',
      email: '',
      phone: '',
      dropoffTime: '',
    }
  }

  fields = {
    name: {
      isRequired: true,
      validator: (value) => {
        if (value === '') {
          return 'Field is required'
        }
      }
    },
    email: {
      isRequired: true,
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
    dropoffTime: {
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
    const {name, phone, email, dropoffTime} = this.state;
    const data = {
      name, email
    }

    const phoneDigits = this.fields.phone.clean(phone);
    if (phoneDigits) {
      data['phone'] = '+1' + phoneDigits;
    }

    const dropoffTimeInfo = this.state.dropoffTimes[parseInt(dropoffTime, 10)]
    data['dropoff_time'] = dropoffTimeInfo ? dropoffTimeInfo.id : '';
    data['dropoff_date'] = dropoffTimeInfo ? dropoffTimeInfo.date : '';
    data['request'] = this.props.request.id;
    data['city'] = 'Los Angeles';

    return data;
  }

  handleSubmit = (event) => {
    event.preventDefault();

    const data = this.getSerializedData();

    axios.post('/api/fulfillments/', data)
      .then((res) => {
        this.setState({
          submitSuccess: true,
          data: data,
        });
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

            // Special cases
            if ( errors['dropoff_time'] || errors['dropoff_date'] ) {
              validationStates['dropoffTime'] = {
                status: 'error',
                msg: 'Please select a valid dropoff time'
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
                    Looks like you've reached the donation limit! :(<br />
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
                    <strong>Problem fulfilling request</strong><br />
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
    const { request } = this.props;

    // Populate dropoff times
    axios.get(`/api/requests/${request.id}/dropoff_times/`)
      .then((res) => {
        this.setState({
          loading: false,
          dropoffTimes: res.data,
        });
      })
      .catch((err) => {
        // TODO: Display error for user
        console.log(err)
      });
  }

  getDropoffTimes = () => {
    const { dropoffTimes } = this.state;

    return dropoffTimes.map((dropoff, index) => {
      const dropoffDate = moment(dropoff.date).format('dddd, LL');
      const dropoffTime = formatTime(dropoff.time_start);
      const location = dropoff.location;
      return (
        <Radio
          key={index}
          name="dropoffTime"
          id="dropoffTime"
          onChange={this.handleInput}
          value={index}
        >
          <strong>{dropoffDate} at {dropoffTime}</strong>
          <br />{location.location_name} <em>({location.neighborhood.name})</em>
          <br />{location.street_address_1}
          <br />{location.city}, {location.state} {location.zipcode}
        </Radio>
      );
    });
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
    const { breakpoints, currentBreakpoint } = this.props;

    if (this.state.loading) {
      return null;
    }
    else if (this.state.submitSuccess) {
      const dropoffTimeInfo = this.state.dropoffTimes[parseInt(this.state.dropoffTime, 10)]
      return <FulfillmentConfirmation info={ this.info } dropoffTime={ dropoffTimeInfo }/>;
    }

    const validationStates = this.state.validationStates;
    const headerMessage = `Great! You are donating ${ this.info.verboseName }.`;

    // Vary button text depending on width
    const confirmButtonText = (
      breakpoints[currentBreakpoint] >= breakpoints.tablet ? 'Confirm Donation' : 'Confirm'
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
          <h2>
            { headerMessage }
            <br />
            Let's work out the details.
          </h2>
        </div>
        <Row>
          <form onSubmit={ this.handleSubmit } className="col-sm-6 col-sm-offset-3">

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
                required
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

            <FormGroup
              controlId="dropoffTime"
              validationState={ validationStates.dropoffTime && validationStates.dropoffTime.status }
              className="dropoff-select"
              onBlur={ this.onBlur }
            >
              <ControlLabel>Choose a Drop Off</ControlLabel>
              { this.getDropoffTimes() }
              { this.getError('dropoffTime') }
            </FormGroup>

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


export default withBreakpoints(FulfillmentForm);
