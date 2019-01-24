import React from 'react';
import { PageHeader } from 'react-bootstrap';
import Logo from './Logo';
import BreadcrumbNav from './BreadcrumbNav';

const header = () => (
  <PageHeader className="header">
    <Logo />
    <BreadcrumbNav />
  </PageHeader>
);

export default header;
