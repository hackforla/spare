import React from 'react';
import { Image } from 'react-bootstrap';
import { useTranslation, Trans } from 'react-i18next';

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

const r = require.context('../../public/assets/teamphotos', false, /\.jpg|png$/);
const images = r.keys().reduce((acc, curr) => {
  acc.push(r(curr));
  return acc;
}, []);

shuffle(images);

const About = () => {
  const { t } = useTranslation('common');

  return (
    <div className="about-page">
      <div className="hero">
        <h2>{t('about.aboutSpare')}</h2>
      </div>
      <div>
        <p className="about-quote">{t('about.quote')}</p>
          <h3>{t('about.label')}</h3>
        <p>{t('about.description')}</p>
        <h3>{t('about.how it work title')}</h3>
        <p>{t('about.how it work')}</p>
        <h3>The team</h3>
        <Trans i18nKey="about.teamBody">
          We are a small team of volunteers with <a href={hackforlaUrl}> Hack for LA </a>. You can contribute to our <a href={githubUrl}>Github project</a> or find us on <a href={slackUrl}>Slack</a>. You can also email us at <a href='mailto:team@whatcanyouspare.org'>team@whatcanyouspare.org</a> but keep in mind that we are volunteers and may be slow to respond.
        </Trans>
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
}

export default About;
