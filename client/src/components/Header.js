import React from 'react';
import { Button, PageHeader } from 'react-bootstrap';
import logo from "./../assets/logo/logo_spare.png";
import { Link, Route, Switch } from "react-router-dom";
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
    <Link to="/">
      <img src={logo} alt="" />
    </Link>
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
