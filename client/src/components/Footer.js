import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => (
    <nav id="Footer">
        <ul>
            <li><Link to="/about">About</Link></li>
            <li><a href="mailto:team@whatcanyouspare.com">Contact</a></li>
        </ul>
    </nav>
);

export default Footer;
