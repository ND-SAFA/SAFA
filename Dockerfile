# pull official base image
FROM node:14-alpine

ARG API_ENDPOINT
RUN test -n "$API_ENDPOINT"

ARG JIRA_CLIENT_ID
ARG JIRA_CLIENT_SECRET
ARG JIRA_REDIRECT_LINK
ARG GITHUB_CLIENT_ID
ARG GITHUB_CLIENT_SECRET
ARG GITHUB_REDIRECT_LINK

# set working directory
WORKDIR /app

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
COPY src /app/src
COPY public /app/public
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY vue.config.js ./

RUN touch ./.env.production && \
  echo -e "\
VUE_APP_API_ENDPOINT=$API_ENDPOINT\n\
VUE_APP_JIRA_CLIENT_ID=$JIRA_CLIENT_ID\n\
VUE_APP_JIRA_CLIENT_SECRET=$JIRA_CLIENT_SECRET\n\
VUE_APP_JIRA_REDIRECT_LINK=$JIRA_REDIRECT_LINK\n\
VUE_APP_GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID\n\
VUE_APP_GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET\n\
VUE_APP_GITHUB_REDIRECT_LINK=$GITHUB_REDIRECT_LINK\n\
" > ./.env.production
RUN cat .env.production

RUN npm install --silent
RUN npm run build
RUN npm install -g serve

RUN npm run lint

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]
