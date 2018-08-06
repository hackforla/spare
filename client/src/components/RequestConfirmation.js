import React from 'react';
import { Image } from "react-bootstrap";
import { Link } from 'react-router-dom';

import RequestIcon from '../assets/icons/requestors/requests.svg';
import EmailIcon from '../assets/icons/requestors/email.svg';
import DonationIcon from '../assets/icons/requestors/donation.svg';

const RequestConfirmation = () => (
  <div className="request-confirmation">
    <div className="hero text-center">
      <h2>Thank you! We posted your request.</h2>
      <p>
        We’ll notify you when we find someone who can get you that item.
        <br />
        Here's what happens next:
      </p>
    </div>
    <div className="container">
      <ol>

        <li>
          <Image src={RequestIcon} />
          <div className="step-text">
            We show your request on <Link to="/">our homepage</Link>
            <span className="disclaimer">(don't worry, it doesn't show any personal info)</span>
          </div>
        </li>

        <li>
          <Image src={EmailIcon} />
          <div className="step-text">
            If someone has this item and wants to donate to you, they'll send us a note.
          </div>
        </li>

        <li>
          <Image src={DonationIcon} />
          <div className="step-text">
            Once that happens, we'll notify you and let you know when and where you can get your item.
          </div>
        </li>

      </ol>
    </div>
  </div>
);

export default RequestConfirmation;
