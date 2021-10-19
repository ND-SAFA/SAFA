ARG DB_HOST=host.docker.internal
ARG DB_USER=user
ARG DB_PASSWORD=secret3
ARG DB_PORT=3306
ARG DB_NAME=safa-db
ARG INSTANCE_CONNECTION_NAME=""

FROM gradle:6.9-jdk11 AS builder

ARG DB_URL
ARG DB_USER
ARG DB_PASSWORD
ARG INSTANCE_CONNECTION_NAME

ARG AppProperties=application-prod.properties
ARG PathToProperties=/app/src/main/resources/$AppProperties

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/

RUN sed -i -e "s,url=,url=$DB_URL,g" $PathToProperties
RUN sed -i -e "s,username=,username=$DB_USER,g" $PathToProperties
RUN sed -i -e "s,password=,password=$DB_PASSWORD,g" $PathToProperties
RUN sed -i -e "s,cloudSqlInstance=,cloudSqlInstance=$INSTANCE_CONNECTION_NAME,g" $PathToProperties

WORKDIR /app
RUN gradle build --stacktrace

FROM openjdk:11

ARG DB_NAME
ARG INSTANCE_CONNECTION_NAME

ENV ENV_DB_NAME=$DB_NAME
ENV ENV_INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME

COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
