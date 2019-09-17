import React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import { withRouter, Link } from 'react-router-dom';

const Footer = () => {
  return (
    <div>
      <nav className="footer">
        <ul>
          <li><LinkContainer to="/about"><Link to="/about">About</Link></LinkContainer></li>
          <li><LinkContainer to="/faqs"><Link to="/faqs">FAQs</Link></LinkContainer></li>
        </ul>
      </nav>
    </div>
  )
};

export default withRouter(Footer);
