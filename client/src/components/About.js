import React from "react";
import { Image } from "react-bootstrap";

import HenaoThumbnail from "../assets/thumbnails/HenaoThumbnail.jpeg";
import AlexaThumbnail from "../assets/thumbnails/AlexaThumbnail.jpeg";
import JeffThumbnail from "../assets/thumbnails/JeffThumbnail.jpeg";
import JordanThumbnail from "../assets/thumbnails/JordanThumbnail.jpeg";
import ShawnThumbnail from "../assets/thumbnails/ShawnThumbnail.jpeg";
import AlliThumbnail from "../assets/thumbnails/AlliThumbnail.jpeg";

let hackforlaUrl = "https://github.com/hackforla";
let githubUrl = "https://github.com/hackforla/spare";
let slackUrl = "https://hackforla.slack.com";

const About = () => (
    <div id="About">
        <h2>About Spare</h2>
        <p>Spare is a project team with 
            <a href={hackforlaUrl}> Hack For La. </a> 
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
            find us on <a href={slackUrl}>Slack.</a> You can
            also email us at team@whatcanyouspare.org but keep in mind that we're
            volunteers and may be slower to respond.  
        </p>
        <div id="team-thumbnails">
            <Image src={HenaoThumbnail} thumbnail/>
            <Image src={AlexaThumbnail} thumbnail/>
            <Image src={JeffThumbnail} thumbnail/>
            <Image src={AlliThumbnail} thumbnail/>
            <Image src={JordanThumbnail} thumbnail/>
            <Image src={ShawnThumbnail} thumbnail/>
        </div>
    </div>
);

export default About;
