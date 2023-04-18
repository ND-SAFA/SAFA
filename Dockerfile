# Step 1 - Create production environment
FROM ubuntu:12.04 as config
ADD src/main/resources /app/src/main/resources
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"

ARG DB_INSTANCE_ARG=hi

RUN if [ ! -z "$DB_INSTANCE_ARG" ] ; \
    then \
      echo "spring.datasource.hikari.data-source-properties.cloudSqlInstance=$DB_INSTANCE_ARG" >> $PathToProperties && \
      echo "spring.datasource.hikari.data-source-properties.socketFactory=com.google.cloud.sql.mysql.SocketFactory" >> $PathToProperties ; \
    fi
RUN cat $PathToProperties

# Step 1 - Install necessary dependencies
FROM gradle:6.9-jdk11 AS builder

# ... - Copy source code
COPY --from=config /app/src/main/resources /app/src/main/resources
ADD src/main/java /app/src/main/java
ADD src/test /app/src/test
ADD build.gradle /app/

# ... - Compile code
WORKDIR /app
RUN gradle build --stacktrace -x Test -x checkstyleMain -x checkstyleTest

# Step - Create endpoint
FROM openjdk:11 AS runner

ENV RUN_SCRIPT="/app/run.sh"

RUN \
    mkdir -p "$(dirname $RUN_SCRIPT)"; \
    touch "$RUN_SCRIPT"; \
    chmod +x "$RUN_SCRIPT"; \
    echo "java -Djava.security.egd=file:/dev/./urandom -jar -Dspring.profiles.active=deployment /app.jar" >> "$RUN_SCRIPT"; \
    cat "$RUN_SCRIPT"

COPY --from=config /app/src/main/resources /app/src/main/resources
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT /bin/bash $RUN_SCRIPT
