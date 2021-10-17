# pull official base image
FROM node:13.12.0-alpine

ARG API_ENDPOINT="localhost"

ENV API_ENDPOINT=$API_ENDPOINT

# set working directory
WORKDIR /app

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
COPY src /app/src
COPY .env ./
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY vue.config.js ./

RUN touch .env.production
RUN sed -i -e "s,VUE_APP_API_ENDPOINT=http://localhost,VUE_APP_API_ENDPOINT=$API_ENDPOINT,g" .env.production

RUN npm install --silent
RUN npm run build
RUN npm install -g serve

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]