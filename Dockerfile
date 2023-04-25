# pull official base image
FROM public.ecr.aws/docker/library/node:14-alpine

# set working directory
WORKDIR /app

# install app dependencies & build
COPY package*.json ./
RUN npm install --silent

# copy files & environment variables
COPY src /app/src
COPY public /app/public
COPY tsconfig.json ./
COPY .eslintrc.js ./
COPY vue.config.js ./
RUN npm run build
RUN npm install -g serve

EXPOSE 80

ENTRYPOINT ["serve", "-p", "80", "-s", "-n", "dist"]
