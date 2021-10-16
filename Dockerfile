FROM gradle:6.9-jdk11 AS builder

ARG DB_HOST=host.docker.internal
ARG DB_USER=user
ARG DB_PASSWORD=secret3
ARG DB_PORT=3306
ARG DB_NAME=safa-db

ARG AppProperties=application-prod.properties
ARG PathToProperties=/app/src/main/resources/$AppProperties

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/

RUN sed -i -e "s,sql.url=,sql.url=jdbc:mysql://$DB_HOST:$DB_PORT/$DB_NAME,g" $PathToProperties
RUN sed -i -e "s,sql.username=,sql.username=$DB_USER,g" $PathToProperties
RUN sed -i -e "s,sql.password=,sql.password=$DB_PASSWORD,g" $PathToProperties
RUN sed -i -e "s,sql.port=,sql.port=$DB_PORT,g" $PathToProperties

WORKDIR /app
RUN gradle build --stacktrace

FROM openjdk:11
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
