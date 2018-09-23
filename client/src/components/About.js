import React from 'react';
import { Image } from 'react-bootstrap';

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
  <div className="about-page">
    <div className="hero">
      <h2>About Spare</h2>
    </div>
    <div>
      <p className="about-quote">"During this homelessness crisis, we believe every gesture of human kindness makes a difference. A jacket not only brings comfort physically but also, it can build a tiny connection that turns a stranger into a friend."</p>
      <h3>About</h3>
      <p>
        Spare connects people in need of clothing and other essentials with people in the community who have things to spare.
        It is like a one-on-one Goodwill. The main objective is to foster interactions between the housed and unhoused.
        We are hoping the donation can be a mechanism for building these connections throughout our community.
      </p>
      <h3>How it works</h3>
      <p>
        There are two main pages, a donation page and a request page. If you want to donate, the donation page houses each request that comes in, and you can fulfill a specific request from there.
        If you’d like to request an item, the request page has categories you can fill out a short form to request. Once there is a match both the requester and donator will receive an email and text on when to pick-up/drop-off the item at the designated donation facility.
        These locations are well known established donation facilities, already in use for general donations.
      </p>
      <h3>The team</h3>
      <p>
        We are a small team of volunteers with <a href={hackforlaUrl}> Hack for LA </a>. You can contribute to our <a href={githubUrl}>Github project</a> or find us on <a href={slackUrl}>Slack</a>.
        You can also email us at <a href="mailto:team@whatcanyouspare.org">team@whatcanyouspare.org</a> but keep in mind that we are volunteers and may be slow to respond.
      </p>
      <div className="team-images">
        {images.map((image, index) => (
          <div className='team-thumbnail' key={index}>
            <Image
              src={image}
            />
          </div>
        ))}
        </div>
      </div>
    </div>
);

export default About;
