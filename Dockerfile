# Creates application-prod.properties with database connection details.
# Copies configuration files to test and build server.
#
FROM ubuntu:12.04 as config

ARG DB_URL=jdbc:mysql://host.docker.internal/safa-db
ARG DB_USER=root
ARG DB_PASSWORD=secret2
ARG DB_INSTANCE

RUN test -n "$DB_URL"
RUN test -n "$DB_USER"
RUN test -n "$DB_PASSWORD"

ARG PathToProperties="/app/src/main/resources/application-prod.properties"

ADD src /app/src

RUN sed -i -e "s,url=,url=$DB_URL,g" $PathToProperties
RUN sed -i -e "s,username=,username=$DB_USER,g" $PathToProperties
RUN sed -i -e "s,password=,password=$DB_PASSWORD,g" $PathToProperties

RUN if [ ! -z "$DB_INSTANCE" ] ; \
    then \
      echo "spring.datasource.hikari.data-source-properties.cloudSqlInstance=$DB_INSTANCE" >> $PathToProperties && \
      echo "spring.datasource.hikari.data-source-properties.socketFactory=com.google.cloud.sql.mysql.SocketFactory" >> $PathToProperties ; \
    fi
RUN cat $PathToProperties

FROM gradle:6.9-jdk11 AS builder

ADD build.gradle /app/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/
COPY --from=config /app/src /app/src

WORKDIR /app
RUN gradle build --stacktrace

# Copy build and configuration settings then create entry point.
#
#
FROM openjdk:11 AS runner
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
