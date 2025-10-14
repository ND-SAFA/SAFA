# pull official base image
FROM public.ecr.aws/docker/library/node:18-alpine

# set working directory
WORKDIR /app

# install app dependencies & build
COPY package*.json ./
RUN npm install --silent
RUN npm install -g serve

# create .env file
ARG API_ENDPOINT

RUN test -n "$API_ENDPOINT"


RUN touch ./.env.production && \
  echo -e "\
VUE_APP_API_ENDPOINT=$API_ENDPOINT\n\
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
