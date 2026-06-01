# Dockerfile
FROM node:16.14.0-alpine

# create destination directory
RUN mkdir -p /var/www/actions-api
WORKDIR /var/www/actions-api

# update and install dependency
RUN apk update && apk upgrade
RUN apk add --no-cache bash git

COPY . /var/www/actions-api/

RUN npm install

COPY . .

EXPOSE 3005

CMD [ "npm", "start" ]