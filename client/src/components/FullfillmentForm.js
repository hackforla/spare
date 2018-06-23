import React, { Component } from 'react';
import axios from 'axios';

import { itemInfo } from '../constants';
import { Button, ControlLabel, FormControl, FormGroup, Radio, Row } from 'react-bootstrap';

class FullfillmentForm extends Component {
  constructor(props, context) {
    // TODO: This is a pretty much a copy paste of RequestForm (we should probably fix that)
    super(props, context);

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.sendForm = this.sendForm.bind(this);

    this.fields = [
      { "key": "name", "name": "Your Name", "type": "text", "placeholder": "Name" },
      { "key": "email", "name": "Your Email", "type": "email", "placeholder": "Email address" },
      { "key": "phone", "name": "Your Phone Number", "type": "text", "placeholder": "Phone number" },
    ];

    //initialize state with keys from fields array
    this.state = {};

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
    var data = {};
    this.fields.forEach((field) => {
      data[field.key] = this.inputs[field.key].value;
    });
    data.item = this.inputs.item.value;
    console.log(data);

    // handle this in development if the API endpoint
    // is on a different port?
    axios.post('http://localhost:8000/api/fullfillments/', data)
      .then((res) => {
        this.setState((oldState) => ({alert: 'success', message: 'Request fullfilled.'}));
        console.log(res);
      })
      .catch((err) => {
        this.setState((oldState) => ({alert: 'danger', message: 'Request fulfillment failed.'}));
        console.log(err)
      });
  }

  getBasicFields(fields){
    return fields.map((field, index) =>
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
    </FormGroup>)
  }

  getItemOptions(items){
    return items.map((item, index) => <option key={index} value={index+1}>{item}</option>)
  }

  render() {
    const { request } = this.props;

    const info = itemInfo[request.item.tag];

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
              <Radio name="pickUp">
                Sunday, April 29th at 10am
              </Radio>
              <Radio name="pickUp">
                Sunday, May 14th at 10am
              </Radio>
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

export default FullfillmentForm;
