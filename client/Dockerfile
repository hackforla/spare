# Base image
FROM node:10

# Create app directory and install packages
WORKDIR /app

# Use live app files
COPY . /app

RUN npm rebuild node-sass
