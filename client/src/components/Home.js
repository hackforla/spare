import React from 'react';
import { Image } from "react-bootstrap";
import { LinkContainer } from 'react-router-bootstrap';
import { Link } from 'react-router-dom';

import BlanketImage from '../assets/home/blanket.svg';


import RequestIcon from '../assets/icons/donors/requests.svg';
import EmailIcon from '../assets/icons/donors/email.svg';
import DonationIcon from '../assets/home/give.png';
//import OldDonationIcon from '../assets/icons/donors/donation.svg';

const Home = () => (
  <div className="home-page">

    <Image src={BlanketImage} width="300" className="intro-image" alt="" />

    <section className="intro-text">
      <h2 className="main-headline">Give spare items directly to people in need, or ask for items if you’re in need of them.</h2>
      <p id="announcement">Now serving Van Nuys (Los Angeles)!</p>
      
      <div className="nav-container">
        <ul className="nav nav-pills nav-justified">
          <li><LinkContainer to="/donate"><Link to="/donate" className="primary">Give an item</Link></LinkContainer></li>
          <li><LinkContainer to="/request"><Link to="/request">Ask for an item</Link></LinkContainer></li>
        </ul>
      </div>
    </section>

    <section className="how-spare-works">
      <h2>How Spare works</h2>
      <p>
        We’re connecting people in need with people who have things to spare. 
      </p>

      <ol>
        <li>
          <Image src={EmailIcon} alt="" className="icon"/><br />
          <strong>Someone requests an item on our website.</strong><br />
          The request is displayed on the website without any personal information.
        </li>
        <li>
          <Image src={RequestIcon} alt="" className="icon"/><br />
          <strong>A donor offers to donate that item.</strong><br />
          We let the recipient know someone is donating the item they need. 
        </li>
        <li>
          <Image src={DonationIcon} alt="" className="icon"/><br />
          <strong>The donor and the recipient meet.</strong><br />
          The donor gives the item to the recipient at a Spare-approved site. 
        </li>
      </ol>

      <p>
        <strong>It’s a simple way to meet and help out your neighbors.</strong>
      </p>
    </section>

  </div>
);

export default Home;
