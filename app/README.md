# Spare App

## Setup Instructions

### 1. Clone project repo

```
git clone https://github.com/hackforla/spare
cd spare/app
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

Find the the server container image (probably `app_server`), and
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

## Import URLs

* Admin - http://localhost:8000/admin/
* Browsable API - http://localhost:8000/api/
* API Login - http://localhost:8000/api-auth/login/
* API Docs - http://localhost:8000/docs/
* Client App - http://localhost:3000/
