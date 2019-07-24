# :tshirt: Spare App [![Build Status](https://travis-ci.org/hackforla/spare.svg?branch=master)](https://travis-ci.org/hackforla/spare)

A project that connects people in need of clothing and other essentials with people in the community who have things to spare. It's kind of like one on one Goodwill. The main objective is to foster interactions between the housed and unhoused. The donation is the mechanism for building these connections throughout our community. \o/

## Table of Contents

- [Project Status](#project-status)
- [Milestones](#milestones)
- [Ways to Contribute](#ways-to-contribute)
- [Setup Instructions](#setup-instructions)
- [Important URLs](#important-urls)
- [Deployment](#deployment)
- [Product and Design Contributors](#product-and-design-contributors)
- [Spare Team](#spare-team)

## Project Status
We are currently aiming to launch Spare sometime in late 2019.

### Milestones
1) Complete core functionality required for launch (In Progress)
2) Prepare demo of app to be presented to partner organizations (TBD)
3) Launch app and begin accepting requests (TBD)

## Ways to Contribute
* Pick up an [engineering task from Github](https://github.com/hackforla/spare/issues)
* Pick up a [design task from Github](https://github.com/hackforla/spare/issues)
* Help us with [product direction or strategy](https://github.com/hackforla/spare#product-and-design-contributors)
* Help us find nonprofit or government partners to help with donation handoff
* Help us find potential users
* Help us define the service design

Also, ping us on the Hack for LA Slack on the #spare channel if you can help. We'd love to have you!

## Setup Instructions

### 1. Clone project repo

```
git clone https://github.com/hackforla/spare
cd spare
```

### 2. Create local env variable file

Copy `.env` to `.env.dev`, then edit dev file
to change SECRET_KEY value.

(Note the SECRET_KEY value, used by django, can be any string you choose)

```
cp .env .env.dev
```

### 3. Install Docker and Docker Compose

Docker

https://docs.docker.com/install/

Docker-Compose

http://docs.docker.com/compose/install/

Create the docker group and add your user

https://docs.docker.com/install/linux/linux-postinstall/

Add the docker group 

`sudo groupadd docker`

Add your user to the docker group

`sudo usermod -aG docker $USER`

### 4. Build Docker images

`docker-compose build`

### 5. Run Docker containers

`docker-compose up`

At any point, `Ctrl-C` stops the containers.

Note: On first setup, the server may sometimes start before the
      database, causing an error. In this case, `Ctrl-C` to stop
      all containers and re-run Docker Compose.

### 6. Access container bash shell
Next, open a second terminal and execute the following command to list all
docker containers currently running:

`docker ps`

Find the the server container image (probably `spare_server`), and
copy the container ID.

Next, execute the following command to access the container's bash shell,
replacing `CONTAINER_ID` with the container's ID hash.

`docker exec -t -i CONTAINER_ID bash`

### 7. Run initial migrations

Once running bash inside of the server container (above), execute the
following to run the initial database migrations:

`python3 manage.py migrate`

### 8. Create a superuser

Execute the following command to create a superuser for the project:

`python3 manage.py createsuperuser`

This will be the main superuser admin for your app.

### Shortcut SetUp Management Command

To run initial migrations, create a superuser, and populate demo data, run this command:

`docker-compose run server python manage.py get_started`

### 9. Login to Django Admin

You can now login to the Django Admin for your user at:

http://localhost:8000/admin/

### 10. Initial database setup

In order for the app to be usable, an admin must create entries in both the `donations/location` and `donations/dropofftime` tables.

## Important URLs

* Admin - http://localhost:8000/admin/
* Browsable API - http://localhost:8000/api/
* API Login - http://localhost:8000/api-auth/login/
* API Docs - http://localhost:8000/docs/
* Client App - http://localhost:3000/

## Deployment

### Staging

https://hackforla-spare-staging.herokuapp.com/

Changes to `staging` branch are automatically deployed to above staging server.

### Production

https://www.whatcanyouspare.org/

Changes to `master` branch are automatically deployed to above production server.

## Product and Design Contributors

Our [project brief is on Google Drive](https://docs.google.com/document/d/124thgq7tZZ-EexYIPA1Bffl7FYm4T2uc4MgKn_IASd0/edit?usp=sharing). We are using [Github issues](https://github.com/hackforla/spare/issues) to track work that needs to be done. Ping Lex Roman on Slack if you are interested in contributing on the product or design side.

* Strategy and research [on Google Drive](https://drive.google.com/drive/folders/1fpH1YDNswWP6DRxHW3QM6MvfKwzWW0ZK?usp=sharing)
* Design files [in this Github repo](https://github.com/hackforla/spare/tree/master/design)
* Prototype [on InVision](https://invis.io/YKH1L8TAB56#/291938149_Home)

## Spare Team

Join our #spare Slack channel -
http://hackforla-slack.herokuapp.com/

Spare Team is
* [@pmfabel](https://github.com/pmfabel)
* [@jimthoburn](https://github.com/jimthoburn)
* [@haydenbetts](https://github.com/haydenbetts)
* [@markmatney](https://github.com/markmatney)
* [@shawnadelic](https://github.com/shawnadelic)
* [@ultraturtle0](https://github.com/ultraturtle0)
* [@ltimin](https://github.com/ltimin)
* [@mfgryan](https://github.com/mfgryan)
* [@calexity](https://github.com/calexity)
* [@allicolyer](https://github.com/allicolyer)
* [@jrkoch](https://github.com/jrkoch)
* [@contrecc](https://github.com/contrecc)
* [@kelseydieterich](https://github.com/kelseydieterich)
* [@tonymichaelhead](https://github.com/tonymichaelhead)

