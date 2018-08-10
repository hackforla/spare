import React from 'react';
import { Button, PageHeader } from 'react-bootstrap';
import { Route, Switch } from "react-router-dom";
import Logo from './Logo';
import BreadcrumbNav from './BreadcrumbNav';
import { LinkContainer } from 'react-router-bootstrap';

const renderFlipButton = (currentSide) => {
  const isFromDonate = (currentSide === 'donate');
  const next = isFromDonate ? 'request' : 'donate';
  const className = `flip-button to-${next}`;
  return () => (
    <span>
      <LinkContainer to={`/${next}`}>
        <Button className={className}>{next} an item</Button>
      </LinkContainer>
    </span>
  );
}

const header = () => (
  <PageHeader className="header">
    <Logo />
    <BreadcrumbNav />
    <Switch>
        <Route
          path="/request"
          render={renderFlipButton('request')}
        />
        <Route
          render={renderFlipButton('donate')}
        />
    </Switch>
  </PageHeader>
);

export default header;
