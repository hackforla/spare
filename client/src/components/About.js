import React from 'react';
import { Col, Row, Image } from 'react-bootstrap';

const hackforlaUrl = 'http://www.hackforla.org/';
const githubUrl = 'https://github.com/hackforla/spare';
const slackUrl = 'https://hackforla.slack.com';

// Thank you, Stack Overflow!
// https://stackoverflow.com/a/12646864
const shuffle = (array) => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (array.length));
    [array[i], array[j]] = [array[j], array[i]]; // eslint-disable-line no-param-reassign
  }
}

const r = require.context('../../public/assets/teamphotos', false, /\.png$/);
const images = r.keys().reduce((acc, curr) => {
  acc.push(r(curr));
  return acc;
}, []);

shuffle(images);


const About = () => (
  <div>
    <h2>About Spare</h2>
    <p>
      Spare is a project team with <a href={hackforlaUrl}>Hack For LA</a>.
      We connect people in need with people who have spare stuff.
    </p>
    <p>
      Our goal is to help those in housing connect and offer help to those
      without housing. During this homelessness crisis, we believe every
      gesture of human kindness makes a difference. A jacket not only brings
      comfort physically but also, it can build a tiny connection that turns
      a stranger into a friend.
    </p>
    <p>
      You can contribute to our <a href={githubUrl}>Github project</a> or
      find us on <a href={slackUrl}>Slack</a>. You can
      also email us at team@whatcanyouspare.org but keep in mind that we're
      volunteers and may be slower to respond.
    </p>
    <Row>
      {images.map((image, index) => (
        <Col sm={4}>
          <Image
            src={image}
            key={index}
            className="team-thumbnail"
          />
        </Col>
        ))}
      </Row>
  </div>
);

export default About;
