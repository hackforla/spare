import React, { useState } from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import { withRouter, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
const Footer = () => {
  const [lang, setLang] = useState('bn');
  const { i18n } = useTranslation();

  const changeLanguage = (e) => {
    const newLang = e.target.value;
    setLang(newLang);
    i18n.changeLanguage(newLang);
  };

  return (
    <div>
      <nav className="footer">
        <ul>
          <li><LinkContainer to="/about"><Link to="/about">About</Link></LinkContainer></li>
          <li><LinkContainer to="/faqs"><Link to="/faqs">FAQs</Link></LinkContainer></li>
          <li>
            <select value={lang} onChange={changeLanguage}>
              <option value="bn">BD</option>
              <option value="en">EN</option>
            </select>
          </li>
        </ul>
      </nav>
    </div>
  )
};

export default withRouter(Footer);
