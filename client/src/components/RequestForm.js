import React, { Component } from 'react';
import axios from 'axios';

import { itemInfo } from '../constants';
import { Alert, Button, ControlLabel, FormControl, FormGroup, Row } from 'react-bootstrap';

import RequestConfirmation from './RequestConfirmation';

class RequestForm extends Component {
  constructor(props, context) {
    super(props, context);

    this.handleChange = this.handleChange.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.sendForm = this.sendForm.bind(this);
    this.getSizeForm = this.getSizeForm.bind(this)

    this.fields = [
      { "key": "name", "name": "Your First Name", "type": "text", "placeholder": "Name" },
      { "key": "email", "name": "Your Email", "type": "email", "placeholder": "Email address" },
      { "key": "phone", "name": "Your Phone Number", "type": "text", "placeholder": "Phone number" },
    ];

    this.state = {
        neighborhoods: []
    };

    //initialize form inputs for submission
    this.inputs = {};

    this.fields.forEach(field => {
      // eslint-disable-next-line
      this.state[field.key] = '';
      this.inputs[field.key] = '';
    });

    this.state.selectValue = this.sizes ? this.sizes[0] : "";

    this.inputs.item = '';
    this.inputs.neighborhood = '';

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

  handleSelect(e) {
    this.setState({selectValue:e.target.value});
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
    data.item = this.props.itemType;
    data.size = this.state.selectValue;
    data.neighborhood = this.inputs.neighborhood.value;

    axios.post('/api/requests/', data)
      .then((res) => {
        this.setState({ submitSuccess: true });
        console.log(res);
      })
      .catch((err) => {
        this.setState({ alert: 'danger', message: 'Request failed.' });
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

  getSizeForm(info){
   return (<FormGroup>
    <ControlLabel>What Size?</ControlLabel>
        <FormControl componentClass="select" placeholder="select" onChange={this.handleSelect}
              value={this.state.selectValue}
        >
              {info.sizeMen && info.sizeMen.map((size, index) => <option key={index} value={size}>{"Mens " + size}</option>)}
              {info.sizeWomen && info.sizeWomen.map((size, index) => <option key={index} value={size}>{"Womens " + size}</option>)}
        </FormControl>
    </FormGroup>)
  }

  getNeighborhoods() {
    return this.state.neighborhoods.map((hood, index) => <option key={index} value={hood.id}>{hood.name}</option>)
  }

  componentDidMount() {
    axios.get('/api/neighborhoods/')
      .then((res) => {
          console.log(res.data);
          this.setState((oldState) => ({neighborhoods: res.data}));
      })
      .catch((err) => console.log(err));
  }

  render() {
    if (this.state.submitSuccess) {
      return <RequestConfirmation />;
    }

    const { itemType } = this.props;

    if (this.state.alert && this.state.message) {
      var formStatus = (
        <Alert bsStyle={this.state.alert}>
          {this.state.message}
        </Alert>
      );
    }

    const info = itemInfo[itemType];
    const pronoun = info.pluralPronoun ? 'those' : 'that'

    const headerMessage = `Cool, let's get you ${pronoun} ${info.verboseName}.`;

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
          <form onSubmit={this.handleSubmit} className="col-sm-6 col-sm-offset-3">
            <FormGroup>
              <ControlLabel>Nearest Neighborhood</ControlLabel>
              <FormControl
                componentClass="select"
                placeholder="select"
                inputRef={(ref) => {this.inputs.neighborhood = ref}}
              >
                {this.getNeighborhoods()}
              </FormControl>
            </FormGroup>
            {this.getBasicFields(this.fields)}
            {(info.sizeMen || info.sizeWomen) ? this.getSizeForm(info) : "" }
            <div className="text-center">
              <Button type="submit">Confirm Request</Button>
            </div>
            {formStatus}
          </form>
        </Row>
      </div>
    );
  }
}

export default RequestForm;
