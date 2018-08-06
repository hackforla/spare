import React from 'react';
import { Button, PageHeader } from 'react-bootstrap';
import { Route, Switch } from "react-router-dom";
import Logo from './Logo';
import { LinkContainer } from 'react-router-bootstrap';

const renderFlipButton = (currentSide) => {
  const isFromDonate = (currentSide === 'donate');
  const next = isFromDonate ? 'request' : 'donate';
  const className = `flip-button to-${next}`;
  return () => (
    <LinkContainer to={`/${next}`}>
      <Button className={className}>{next} an item</Button>
    </LinkContainer>
  );
}

const header = () => (
  <PageHeader className="header">
    <Logo />
    <Switch>
        <Route
          path="/donate"
          render={renderFlipButton('donate')}
        />
        <Route
          path="/request"
          render={renderFlipButton('request')}
        />
    </Switch>
  </PageHeader>
);

export default header;
