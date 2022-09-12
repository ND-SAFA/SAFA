# Step 1 - Install necessary dependencies
FROM gradle:6.9-jdk11 AS builder
ADD src /app/src
ADD build.gradle /app/
RUN gradle build --stacktrace -x test -x checkstyleMain -x checkstyleTest

# Step 2 - Create production environment
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"
FROM ubuntu:12.04 as config

ARG DB_URL=jdbc:mysql://host.docker.internal/safa-db
ARG DB_USER=root
ARG DB_PASSWORD=secret2
ARG DB_INSTANCE
ARG JWT_KEY=3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShV

RUN test -n "$DB_URL"
RUN test -n "$DB_USER"
RUN test -n "$DB_PASSWORD"
RUN test -n "$JWT_KEY"


RUN sed -i -e "s,url=,url=$DB_URL,g" $PathToProperties
RUN sed -i -e "s,username=,username=$DB_USER,g" $PathToProperties
RUN sed -i -e "s,password=,password=$DB_PASSWORD,g" $PathToProperties
RUN sed -i -e "s,jwt.key=,jwt.key=$JWT_KEY,g" $PathToProperties
RUN sed -i -e "s,jwt.key=,jwt.key=$JWT_KEY,g" $PathToProperties

RUN if [ ! -z "$DB_INSTANCE" ] ; \
    then \
      echo "spring.datasource.hikari.data-source-properties.cloudSqlInstance=$DB_INSTANCE" >> $PathToProperties && \
      echo "spring.datasource.hikari.data-source-properties.socketFactory=com.google.cloud.sql.mysql.SocketFactory" >> $PathToProperties ; \
    fi
RUN cat $PathToProperties


ADD checkstyle.xml /app/

COPY --from=config /app/src /app/src


# Step - Test application
WORKDIR /app
ADD resources/ /app/resources/

# Copy build and configuration settings then create entry point.
#
#
FROM openjdk:11 AS runner
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
