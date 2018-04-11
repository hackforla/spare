# Base image
FROM node:6

# Create app directory and install packages
WORKDIR /app
COPY package.json /app/package.json
RUN npm install --quiet

# Use live app files
COPY . /app
