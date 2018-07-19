import React, { Component } from 'react';
import axios from 'axios';
import moment from 'moment';

import { itemInfo } from '../constants';
import FulfillmentConfirmation from './FulfillmentConfirmation';
import { Button, ControlLabel, FormControl, FormGroup, Radio, Row } from 'react-bootstrap';

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
    const length = this.state[key].length;
    if (length > 10) return 'success';
    else if (length > 5) return 'warning';
    else if (length > 0) return 'error';
    return null;
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

    data.dropoff_time = selectedDropoff.id;
    data.dropoff_date = selectedDropoff.date;
    data.request = this.props.request.id;
    data.city = 'Los Angeles';

    // handle this in development if the API endpoint
    // is on a different port?
    axios.post('http://localhost:8000/api/fulfillments/', data)
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

    axios.get(`http://localhost:8000/api/requests/${request.id}/dropoff_times/`)
      .then((res) => {
          this.setState({
            dropoffs: res.data
          });
      });
  }

  render() {
    const { request } = this.props;

    const info = itemInfo[request.item.tag];

    if (this.state.submitSuccess) {
      const { responseData, selectedDropoff } = this.state;

      return <FulfillmentConfirmation data={ responseData } info={ info } dropoff={ selectedDropoff }/>;
    }

    const headerMessage = `Great! You are donating ${ info.verboseName }.`;

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
              <Button type="submit">Confirm Donation</Button>
            </div>
          </form>
        </Row>
      </div>
    );
  }
}

export default FulfillmentForm;
