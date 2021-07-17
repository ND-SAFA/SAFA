FROM gradle:5.6.2-jdk8 AS builder
COPY checkstyle.xml /app/checkstyle.xml

ARG _MY_SQL_HOST
ARG _MY_SQL_USERNAME
ARG _MY_SQL_PASSWORD
ARG _MY_SQL_CONNECTION_NAME
ARG _MY_SQL_DATABASE
ARG _NEO4J_URI
ARG _NEO4J_USERNAME
ARG _NEO4J_PASSWORD
ARG GOOGLE_APPLICATION_CREDENTIALS

COPY .env /app/.env
COPY safa-google-key.json /app/safa-google-key.json

WORKDIR /app
ADD build.gradle /app/
ADD src/ /app/src/
RUN gradle build --stacktrace

FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
