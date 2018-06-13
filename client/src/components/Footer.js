import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => (
    <div id="Footer">
        <Link to="/about">About</Link>
        &nbsp;&nbsp;
        <a href="mailto:team@whatcanyouspare.com">Contact</a>
    </div>
);

export default Footer;
