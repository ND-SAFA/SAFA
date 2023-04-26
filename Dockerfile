# pull official base image
FROM public.ecr.aws/docker/library/node:14-alpine

# set working directory
WORKDIR /app

# install app dependencies & build
COPY package*.json ./
RUN npm install --silent
RUN npm install -g serve

# create .env file
ARG API_ENDPOINT
ARG JIRA_CLIENT_ID
ARG JIRA_REDIRECT_LINK
ARG GITHUB_CLIENT_ID
ARG GITHUB_REDIRECT_LINK

RUN test -n "$API_ENDPOINT"


RUN touch ./.env.production && \
  echo -e "\
VUE_APP_API_ENDPOINT=$API_ENDPOINT\n\
VUE_APP_JIRA_CLIENT_ID=$JIRA_CLIENT_ID\n\
VUE_APP_JIRA_REDIRECT_LINK=$JIRA_REDIRECT_LINK\n\
VUE_APP_GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID\n\
VUE_APP_GITHUB_REDIRECT_LINK=$GITHUB_REDIRECT_LINK\n\
" > ./.env.production
RUN cat .env.production

# copy files & environment variables
COPY src /app/src
COPY public /app/public
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY vue.config.js ./
RUN npm run build

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]
