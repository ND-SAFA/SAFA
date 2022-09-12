# Step 1 - Install necessary dependencies
FROM gradle:6.9-jdk11 AS builder

# ... - Copy source code
ADD src/main/java /app/src/main/java
ADD src/test /app/src/test
ADD build.gradle /app/

# ... - Compile code
WORKDIR /app
RUN gradle build --stacktrace -x Test -x checkstyleMain -x checkstyleTest

# Step 2 - Create production environment
FROM ubuntu:12.04 as config
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"

ARG DB_URL=jdbc:mysql://host.docker.internal/safa-db
ARG DB_USER=root
ARG DB_PASSWORD=secret2
ARG DB_INSTANCE
ARG JWT_KEY=3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShV
ARG TGEN_ENDPOINT=https://tgen-dev-5asg6qsnba-uc.a.run.app

RUN test -n "$DB_URL" && sed -i -e "s,url=,url=$DB_URL,g" $PathToProperties
RUN test -n "$DB_USER" && sed -i -e "s,username=,username=$DB_USER,g" $PathToProperties
RUN test -n "$DB_PASSWORD" && sed -i -e "s,password=,password=$DB_PASSWORD,g" $PathToProperties
RUN test -n "$JWT_KEY" && sed -i -e "s,jwt.key=,jwt.key=$JWT_KEY,g" $PathToProperties
RUN test -n "$TGEN_ENDPOINT" && sed -i -e "s,tgen.endpoint=,tgen.endpoint=$TGEN_ENDPOINT,g" $PathToProperties

RUN if [ ! -z "$DB_INSTANCE" ] ; \
    then \
      echo "spring.datasource.hikari.data-source-properties.cloudSqlInstance=$DB_INSTANCE" >> $PathToProperties && \
      echo "spring.datasource.hikari.data-source-properties.socketFactory=com.google.cloud.sql.mysql.SocketFactory" >> $PathToProperties ; \
    fi
RUN cat $PathToProperties

# Step - Lint source code
ADD checkstyle.xml /app/
RUN gradle checkstyleMain

# Step - Test application
ADD resources/ /app/resources/
RUN gradle test

# Step - Create endpoint
FROM openjdk:11 AS runner
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=prod","/app.jar"]
