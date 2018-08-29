import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
    //TODO underline the active link
    //let linkStyle = {
    //    borderBottom: '2px solid #CCC',
    //    padding: '0 0 2px 1px',
    //}
    return (
        <nav id="Footer">
            <ul>
                <li><Link to="/donate">Donate</Link></li>
                <li><Link to="/request">Request</Link></li>
                <li><Link to="/about">About</Link></li>
                <li><a href="mailto:team@whatcanyouspare.com">Contact</a></li>
            </ul>
        </nav>
    )
};

export default Footer;
