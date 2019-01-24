import React from 'react';
import { Image } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { withRouter, Route, Link } from 'react-router-dom';

import LearnMoreIcon from '../assets/icons/donors/learnmore.svg';

const Footer = () => {
  return (
    <div>
      <nav className="footer">
        <ul>
          <li><LinkContainer to="/about"><Link to="/about">About</Link></LinkContainer></li>
          <li><a href="mailto:team@whatcanyouspare.org">Contact</a></li>
        </ul>
      </nav>
    </div>
  )
};

export default withRouter(Footer);
