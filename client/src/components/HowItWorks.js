import React from 'react';
import { Image } from "react-bootstrap";
import { Link } from 'react-router-dom';
import { Col, Row } from 'react-bootstrap';

import RequestIcon from '../assets/icons/donors/requests.svg';
import EmailIcon from '../assets/icons/donors/email.svg';
import DonationIcon from '../assets/icons/donors/donation.svg';

const HowItWorks = () => (
  <div className="how-it-works">
    <div className="hero text-center">
      <h2>How Spare works</h2>
      <p>
        We’re connecting people in need with people who have things to spare. 
      </p>
    </div>
    <Row>
      <Col sm={8} smOffset={2} className="step-column">
        <ol>
          <li>
            <Image src={EmailIcon} />
            <div className="step-text">
              Someone requests an item on our website
            </div>
          </li>

          <li>
            <Image src={RequestIcon} />
            <div className="step-text">
              A donor offers to donate that item.
              <span className="additional-text">We let the recipient know someone is donating the item they need. </span>
            </div>
          </li>

          <li>
            <Image src={DonationIcon} />
            <div className="step-text">
              The donor and the recipient meet at a location we provide to exchange the item.
              <span className="additional-text">
                You’ll meet at a nonprofit’s site at a specific time. It’s very easy and nice. You get to meet more of your neighbors.
              </span>
            </div>
          </li>

        </ol>
      </Col>
    </Row>
  </div>
);

export default HowItWorks;
