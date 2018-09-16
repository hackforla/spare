import React from 'react';
import { PageHeader } from 'react-bootstrap';
import Logo from './Logo';
import BreadcrumbNav from './BreadcrumbNav';

const header = () => (
  <PageHeader className="header">
    <div className="notification">
      <p className="text">Now serving Hollywood and Highland Park!</p>
    </div>
    <Logo />
    <BreadcrumbNav />
  </PageHeader>
);

export default header;
