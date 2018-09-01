import React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <nav className="footer">
      <ul>
        <li><LinkContainer to="/donate"><Link to="/donate">Donate</Link></LinkContainer></li>
        <li><LinkContainer to="/request"><Link to="/request">Request</Link></LinkContainer></li>
        <li><LinkContainer to="/about"><Link to="/about">About</Link></LinkContainer></li>
        <li><a href="mailto:team@whatcanyouspare.com">Contact</a></li>
      </ul>
    </nav>
  )
};

export default Footer;
