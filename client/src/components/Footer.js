import React from 'react';
import { Image } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { withRouter, Route, Link } from 'react-router-dom';

import LearnMoreIcon from '../assets/icons/donors/learnmore.svg';

const Footer = () => {
  const learnMore = (
    <div className="learn-more"><Link to="/how-it-works"><Image src={ LearnMoreIcon }/>Learn more</Link> about how donations work</div>
  );
  return (
    <div>
      <Route path="/(donate|request|about)/" render={(props) => learnMore }/>
      <nav className="footer">
        <ul>
          <li><LinkContainer to="/donate"><Link to="/donate">Donate</Link></LinkContainer></li>
          <li><LinkContainer to="/request"><Link to="/request">Request</Link></LinkContainer></li>
          <li><LinkContainer to="/about"><Link to="/about">About</Link></LinkContainer></li>
          <li><a href="mailto:team@whatcanyouspare.org">Contact</a></li>
        </ul>
      </nav>
    </div>
  )
};

export default withRouter(Footer);
