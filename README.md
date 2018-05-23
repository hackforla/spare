# Spare App [![Build Status](https://travis-ci.org/hackforla/spare.svg?branch=master)](https://travis-ci.org/hackforla/spare)

## Setup Instructions

### 1. Clone project repo

```
git clone https://github.com/hackforla/spare
cd spare
```

### 2. Create local env variable file

Copy `.env` to `.env.dev`, then edit dev file
to change SECRET_KEY value.

```
cp .env .env.dev
```

### 3. Install Docker and Docker Compose

Docker

https://docs.docker.com/install/

Docker-Compose

http://docs.docker.com/compose/install/

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

### 9. Login to Django Admin

You can now login to the Django Admin for your user at:

http://localhost:8000/admin/

## Important URLs

* Admin - http://localhost:8000/admin/
* Browsable API - http://localhost:8000/api/
* API Login - http://localhost:8000/api-auth/login/
* API Docs - http://localhost:8000/docs/
* Client App - http://localhost:3000/

## Product and Design Contributors

Our [project brief is on Google Drive](https://docs.google.com/document/d/124thgq7tZZ-EexYIPA1Bffl7FYm4T2uc4MgKn_IASd0/edit?usp=sharing). We are using [Github issues](https://github.com/hackforla/spare/issues) to track work that needs to be done. Ping Lex Roman on Slack if you are interested in contributing on the product or design side.


* Strategy and research [on Google Drive](https://drive.google.com/drive/folders/1fpH1YDNswWP6DRxHW3QM6MvfKwzWW0ZK?usp=sharing)
* Design files [in this Github repo](https://github.com/hackforla/spare/tree/master/design)
* Prototype [on InVision](https://invis.io/YKH1L8TAB56#/291938149_Home)

## Spare Team

Join our #spare Slack channel -
http://hackforla-slack.herokuapp.com/

Spare Team is
* [@shawnadelic](https://github.com/shawnadelic)
* [@ultraturtle0](https://github.com/@ultraturtle0)
* [@ltimin](https://github.com/@ltimin)
* [@mfgryan](https://github.com/@mfgryan)
* [@vonetta](https://github.com/@vonetta)
* [@himalchoi](https://github.com/@himalchoi)
* [@calexity](https://github.com/@calexity)
