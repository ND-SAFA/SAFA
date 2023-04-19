# pull official base image
FROM public.ecr.aws/docker/library/node:14-alpine

# set working directory
WORKDIR /app

# copy files & environment variables
COPY package*.json ./
COPY src /app/src
COPY public /app/public
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY vue.config.js ./

# install app dependencies & build
RUN npm install --silent
RUN npm run build
RUN npm install -g serve

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]
