import React from 'react';
import { Image } from "react-bootstrap";
import { Col, Row } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { withRouter, Route, Link } from 'react-router-dom';

import BlanketImage from '../assets/home/blanket.svg';

import RequestIcon from '../assets/icons/donors/requests.svg';
import EmailIcon from '../assets/icons/donors/email.svg';
import DonationIcon from '../assets/icons/donors/donation.svg';

const Home = () => (
  <div>

    <Image src={BlanketImage} width="200" alt="" />
  
    <h2>Give spare items directly to people in need, or ask for items if you’re in need of them.</h2>
    <p>Now serving Van Nuys (Los Angeles)!</p>
    
    <ul>
      <li><LinkContainer to="/donate"><Link to="/donate">Give an item</Link></LinkContainer></li>
      <li><LinkContainer to="/request"><Link to="/request">Ask for an item</Link></LinkContainer></li>
    </ul>

    <h2>How Spare works</h2>
    <p>
      We’re connecting people in need with people who have things to spare. 
    </p>

    <ol>
      <li>
        <Image src={EmailIcon} alt="" /><br />
        <strong>Someone requests an item on our website.</strong>
        The request is displayed on the website without any personal information.
      </li>
      <li>
        <Image src={RequestIcon} alt="" /><br />
        <strong>A donor offers to donate that item.</strong>
        We let the recipient know someone is donating the item they need. 
      </li>
      <li>
        <Image src={DonationIcon} alt="" /><br />
        <strong>The donor gives the item to the recipient. </strong>
        The donor and recipent meet at a nonprofit site we provide to exchange the item. 
      </li>
    </ol>
  
    <p>
      It’s a simple way to meet and help out your neighbors.
    </p>
  
  </div>
);

export default Home;
