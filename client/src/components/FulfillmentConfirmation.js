import React, { Component } from 'react';
import moment from 'moment';

const now = moment();

// TODO: This is copied/pasted from fulfillment form (refactor)
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

class FulfillmentConfirmation extends Component {
  render() {
    const { dropoff, info } = this.props;
    const { date, location, time_start } = dropoff;

    const { pluralPronoun, verboseName } = info;

    let itemDescription;

    if (!pluralPronoun) {
      itemDescription = `a ${ verboseName }`;
    }
    else {
      itemDescription = verboseName;
    }

    const formattedDate = moment(date).format('dddd, LL');
    const formattedTime = formatTime(time_start);

    return (
      <div className="fulfillment-confirmation">
        <div className="hero text-center">
          <h2>Thank you! We'll let your recipient know that you're donating { itemDescription }.</h2>
          <p>
            Please drop the item off at { location.location_name } on { formattedDate } at { formattedTime }.
          </p>
        </div>
      </div>
    );
  }
}

export default FulfillmentConfirmation;
