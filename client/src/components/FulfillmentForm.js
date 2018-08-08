import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import { emailRegex, itemInfo } from '../utils/constants';
import FulfillmentConfirmation from './FulfillmentConfirmation';
import { Alert, Button, ControlLabel, FormControl, FormGroup, Radio, Row } from 'react-bootstrap';
import { withBreakpoints } from 'react-breakpoints';

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
  constructor(props, context) {
    // TODO: This is a pretty much a copy paste of RequestForm (we should probably fix that)
    super(props, context);

    this.onChangeDropoffs = this.onChangeDropoffs.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.sendForm = this.sendForm.bind(this);

    this.fields = [
      { "key": "name", "name": "Your First Name", "type": "text", "placeholder": "Name" },
      { "key": "email", "name": "Your Email", "type": "email", "placeholder": "Email address" },
      { "key": "phone", "name": "Your Phone Number", "type": "text", "placeholder": "Phone number" },
    ];

    //initialize state with keys from fields array
    this.state = {
        dropoffs: []
    };

    //initialize form inputs for submission
    this.inputs = {};

    this.fields.forEach(field => {
      // eslint-disable-next-line
      this.state[field.key] = '';
      this.inputs[field.key] = '';
    });

    this.inputs.item = '';

  }

  // Example validation of the inputs
  getValidationState(key) {
    var input = this.state[key];
    if (!input) return null;
    if (key === 'phone') {
        var phone_num = /^\+(\d+)\d{10}/.exec(input); 
        var all_num = /^(\d{10})$/.exec(input);
        if (phone_num || all_num) return 'success';
        else return 'error';
    }
    if (key === 'email') {
        return (emailRegex.test(input) ? 'success' : 'error');
    }
    if (key === 'name') return (/^[A-Za-z\s]+$/.test(input) ? 'success' : 'error');

  }

  handleChange(e, key) {
    let newState = {};
    newState[key] = e.target.value
    this.setState(newState);
  }

  // Display message and run callback on form submission
  handleSubmit(e) {
    e.preventDefault();
    this.setState({
      alert: 'info',
      message: 'Sending...'
    }, this.sendForm);
  }

  // Send HTTP post request
  sendForm() {
    const { dropoffs } = this.state;

    var data = {};

    this.fields.forEach((field) => {
      data[field.key] = this.inputs[field.key].value;
    });

    const selectedDropoff = dropoffs[this.inputs.dropoff_time - 1];

    if (!this.inputs.dropoff_time) {
        this.setState({alert: 'warning', message: 'Please select a dropoff location and time.'});
        return;
    }   

    data.dropoff_time = selectedDropoff.id;
    data.dropoff_date = selectedDropoff.date;
    data.request = this.props.request.id;
    data.city = 'Los Angeles';


    if (!(data.phone || data.email)) {
        this.setState({alert: 'warning', message: 'Please provide either a phone or email address.'});
        return;
    }

    if (data.email && !(emailRegex.test(data.email))) {
        this.setState({alert: 'warning', message: 'Please enter a valid email.'});
        return;
    }

    if (!(/^[A-Za-z\s]+$/.test(data.name))) {
        this.setState({alert: 'warning', message: 'Please enter a valid first name.'});
        return;
    }


    var phone_num = /^\+(\d+)\d{10}/.exec(data.phone); 
    var all_num = /^(\d{10})$/.exec(data.phone);
    if (!phone_num) {
      if (!all_num) {
          this.setState({alert: 'warning', message: 'Please enter a valid phone number.'});
          return;
      }
      data.phone = '+1' + data.phone;
    }

    console.log(data);


    // handle this in development if the API endpoint
    // is on a different port?
    axios.post('/api/fulfillments/', data)
      .then((res) => {
        this.setState({
          submitSuccess: true,
          responseData: res.data,
          selectedDropoff: selectedDropoff,
        });
        console.log(res);
      })
      .catch((err) => {
        this.setState((oldState) => ({alert: 'danger', message: 'Request fulfillment failed.'}));
        console.log(err)
      });
  }

  getBasicFields(fields) {
    return fields.map((field, index) => (
      <FormGroup controlId={field.key} key={index}
        validationState={this.getValidationState(field.key)}>
        <ControlLabel>{field.name}</ControlLabel>
        <FormControl
          type={field.type}
          value={this.state[field.key]}
          placeholder={field.placeholder}
          inputRef={(ref) => {this.inputs[field.key] = ref}}
          onChange={event => {this.handleChange(event, field.key)}}
        />
        <FormControl.Feedback />
      </FormGroup>
    ))
  }

  getItemOptions(items){
    return items.map((item, index) => <option key={index} value={index+1}>{item}</option>)
  }

  onChangeDropoffs(e) {
    this.inputs.dropoff_time = e.target.value;
  }

  renderDropOffs() {
    const { dropoffs } = this.state;
    return dropoffs.map((dropoff, index) => {
      const dropoffDate = moment(dropoff.date).format('dddd, LL');
      const dropoffTime = formatTime(dropoff.time_start);
      return (
        <Radio
          key={index}
          name="pickUp"
          onChange={this.onChangeDropoffs}
          value={index+1}
        >
          {dropoff.location.organization_name} - {dropoffDate} at {dropoffTime}
        </Radio>
      );
    });
  }

  componentDidMount() {
    const { request } = this.props;

    axios.get(`/api/requests/${request.id}/dropoff_times/`)
      .then((res) => {
          this.setState({
            dropoffs: res.data
          });
      });
  }

  render() {
    const { breakpoints, currentBreakpoint, request } = this.props;

    const info = itemInfo[request.item.tag];

    if (this.state.submitSuccess) {
      const { responseData, selectedDropoff } = this.state;

      return <FulfillmentConfirmation data={ responseData } info={ info } dropoff={ selectedDropoff }/>;
    }

    if (this.state.alert && this.state.message) {
      var formStatus = (
        <Alert bsStyle={this.state.alert}>
          {this.state.message}
        </Alert>
      );
    }

    const headerMessage = `Great! You are donating ${ info.verboseName }.`;

    const confirmButtonText = (
      breakpoints[currentBreakpoint] >= breakpoints.tablet ? 'Confirm Donation' : 'Confirm'
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
          <form onSubmit={this.handleSubmit} className="col-sm-6 col-sm-offset-3">
            {this.getBasicFields(this.fields)}
            <FormGroup>
              <ControlLabel>Choose a drop off</ControlLabel>
              {this.renderDropOffs()}
            </FormGroup>
            <div className="text-center">
              <Button type="submit">{ confirmButtonText }</Button>
            </div>
            {formStatus}
          </form>
        </Row>
      </div>
    );
  }
}

export default withBreakpoints(FulfillmentForm);
