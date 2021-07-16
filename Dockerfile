FROM gradle:5.6.2-jdk8 AS builder
COPY checkstyle.xml /app/checkstyle.xml

ENV _MY_SQL_HOST=$_MY_SQL_HOST
ENV _MY_SQL_USERNAME=$_MY_SQL_USERNAME
ENV _MY_SQL_PASSWORD=$_MY_SQL_PASSWORD
ENV _MY_SQL_CONNECTION_NAME=$_MY_SQL_CONNECTION_NAME
ENV _MY_SQL_DATABASE=$_MY_SQL_DATABASE
ENV _NEO4J_URI=$_NEO4J_URI
ENV _NEO4J_USERNAME=$_NEO4J_USERNAME
ENV _NEO4J_PASSWORD=$_NEO4J_PASSWORD
ENV GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS

COPY .env /app/.env
COPY safa-google-key.json /app/safa-google-key.json

WORKDIR /app
ADD build.gradle /app/
ADD src/ /app/src/
RUN gradle build --stacktrace

FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
