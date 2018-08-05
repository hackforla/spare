#!/usr/bin/env bash

CLIENT_BUILD_DIR=/app/build
SERVER_TEMPLATES_DIR=/app/server/core/templates
SERVER_STATIC_DIR=/app/server/core/static

# Move index.html
mkdir -p $SERVER_TEMPLATES_DIR
cp -r $CLIENT_BUILD_DIR/index.html $SERVER_TEMPLATES_DIR

# This is easier than trying to change create-react-app's build behavior
sed -i 's/\/manifest.json/\/static\/manifest.json/' $SERVER_TEMPLATES_DIR/index.html
sed -i 's/\/favicon.ico/\/static\/favicon.ico/' $SERVER_TEMPLATES_DIR/index.html

# Move assets and static directories
mkdir -p $SERVER_STATIC_DIR
cp -r $CLIENT_BUILD_DIR/static/* $SERVER_STATIC_DIR
mkdir -p $SERVER_STATIC_DIR/assets
cp -r $CLIENT_BUILD_DIR/assets $SERVER_STATIC_DIR
cp $CLIENT_BUILD_DIR/favicon.ico $SERVER_STATIC_DIR
cp $CLIENT_BUILD_DIR/manifest.json $SERVER_STATIC_DIR
cp $CLIENT_BUILD_DIR/asset-manifest.json $SERVER_STATIC_DIR
cp $CLIENT_BUILD_DIR/service-worker.js $SERVER_STATIC_DIR
