import React, { Component } from 'react';

import { FormGroup, ControlLabel, FormControl, Button } from 'react-bootstrap';

class RequestForm extends Component {

	constructor(props, context) {
		super(props, context);

		this.handleChange = this.handleChange.bind(this);
        
        this.fields = [
            { "key": "name", "name": "Full Name", "type": "text", "placeholder": "Enter name" },
			{ "key": "email", "name": "Email", "type": "email", "placeholder": "Enter Email" },
            { "key": "phone", "name": "Phone Number", "type": "text", "placeholder": "Enter Phone Number" },
        ];

        this.itemOptions = ["hygiene","essentials","clothing"];
        
        //initialize state with keys from fields array
        this.state = {};
        this.fields.forEach(field => {
            this.state[field.key] = ''; 
        });

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

    getBasicFields(fields){
        return fields.map((field, index) =>
            <FormGroup controlId={field.key} key={index}
            validationState={this.getValidationState(field.key)}>
                <ControlLabel>{field.name}</ControlLabel>
                <FormControl
                    type={field.type}
                    value={this.state[field.key]}
                    placeholder={field.placeholder}
                    onChange={event => {this.handleChange(event, field.key)}}
                />
                <FormControl.Feedback />
            </FormGroup>)
    }

    getItemOptions(items){
        return items.map(item => <option value={item}>{item}</option>)
    }
	
    render() {
        return (
            <div className="RequestForm">
                <h2>Request form</h2>
                <form>
                    {this.getBasicFields(this.fields)}
                    <FormGroup>
                        <ControlLabel>Select an Item</ControlLabel>
                        <FormControl componentClass="select" placeholder="select">
                            {this.getItemOptions(this.itemOptions)}
                        </FormControl>
                    </FormGroup>
                    <Button type="submit">Submit</Button>
                </form>
            </div>
        );
    }
}

export default RequestForm;
