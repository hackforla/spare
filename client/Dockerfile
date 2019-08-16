# Base image
FROM node:8

# Create app directory and install packages
WORKDIR /app

# Use live app files
COPY . /app

RUN npm rebuild node-sass
