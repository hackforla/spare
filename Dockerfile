# Build client application
FROM node:6 AS build

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY client/package.json /app/package.json

RUN npm install react-scripts@3.0.1 -g --silent
RUN npm install --silent

COPY client /app

RUN npm run build

# Build main image
FROM python:3.6

WORKDIR /app

# Use python -u/unbuffered setting
ENV PYTHONUNBUFFERED 1

# Install requirements
COPY server/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# NOTE: This needs to be improved, but works for now
COPY --from=build /app/server/core/templates/index.html /app/core/templates/index.html
COPY --from=build /app/server/core/static /app/core/static
COPY --from=build /app/build/assets /app/core/static
COPY --from=build /app/build/favicon.ico /app/core/static
COPY --from=build /app/build/manifest.json /app/core/static
COPY --from=build /app/build/asset-manifest.json /app/core/static
COPY --from=build /app/build/service-worker.js /app/core/static

COPY server /app
