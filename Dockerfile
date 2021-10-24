FROM gradle:6.9-jdk11 AS builder

ARG DB_URL=jdbc:mysql://localhost:3606/safa-db
ARG DB_USER=user
ARG DB_PASSWORD=secret3

RUN test -n "$DB_URL"
RUN test -n "$DB_USER"
RUN test -n "$DB_PASSWORD"

ARG PathToProperties="/app/src/main/resources/application-prod.properties"

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/

RUN sed -i -e "s,url=,url=$DB_URL,g" $PathToProperties
RUN sed -i -e "s,username=,username=$DB_USER,g" $PathToProperties
RUN sed -i -e "s,password=,password=$DB_PASSWORD,g" $PathToProperties

WORKDIR /app
RUN gradle build --stacktrace

FROM openjdk:11

COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
