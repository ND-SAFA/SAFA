# pull official base image
FROM node:14-alpine

ARG API_ENDPOINT
ARG JIRA_CLIENT_ID
ARG JIRA_CLIENT_SECRET
ARG JIRA_REDIRECT_LINK
ARG GITHUB_CLIENT_ID
ARG GITHUB_CLIENT_SECRET
ARG GITHUB_REDIRECT_LINK
ARG DDOG_APP_ID
ARG DDOG_DDOG_TOKEN

# set working directory
WORKDIR /app

# copy files & environment variables
COPY package*.json ./
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
VUE_APP_DDOG_APP_ID=$DDOG_APP_ID\n\
VUE_APP_DDOG_DDOG_TOKEN=$DDOG_DDOG_TOKEN\n\
" > ./.env.production
RUN cat .env.production

# install app dependencies & build
RUN npm install --silent
RUN npm run build
RUN npm install -g serve

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]
