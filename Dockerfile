# Step 1 - Create production environment
FROM ubuntu:12.04 as config
ADD src/main/resources /app/src/main/resources
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"

ARG DB_INSTANCE_ARG

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

# Step - Lint source code
ADD checkstyle.xml /app/
RUN gradle checkstyleMain

# Step - Test application
ADD resources/ /app/resources/
RUN gradle test

# Step - Create endpoint
FROM openjdk:11 AS runner

ARG DB_URL_ARG=jdbc:mysql://host.docker.internal/safa-db
ARG DB_USER_ARG=root
ARG DB_PASSWORD_ARG=secret2
ARG JWT_KEY_ARG=3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShV
ARG TGEN_ENDPOINT_ARG=http://35.184.232.43
ARG JIRA_REDIRECT_LINK_ARG="https://localhost.safa.ai:8080/create?tab=jira"
ARG JIRA_CLIENT_ID_ARG="lWzIreg3PMSqkjkkvKyqR6xvHJDXvRAF"
ARG JIRA_SECRET_ARG="YhfXF-mR0-ZZoH1RD0T504nAfAB002dNVmsmd-JES3LL3_X6kvebRUWh3Ja0IgdT"
ARG GITHUB_CLIENT_ID_ARG="Iv1.75905e8f5ace1f4b"
ARG GITHUB_SECRET_ARG="2d6bd433619bebf523cef951bd1296ac2d2795c3"

RUN \
    if [ ! -z "$DB_URL_ARG" ]; then export DB_ARG="$DB_URL_ARG"; fi; \
    if [ ! -z "$DB_USER_ARG" ]; then export DB_USER="$DB_USER_ARG"; fi; \
    if [ ! -z "$DB_PASSWORD_ARG" ]; then export DB_PASSWORD="$DB_PASSWORD_ARG"; fi; \
    if [ ! -z "$JWT_KEY_ARG" ]; then export JWT_KEY="$JWT_KEY_ARG"; fi; \
    if [ ! -z "$TGEN_ENDPOINT_ARG" ]; then export TGEN_ENDPOINT="$TGEN_ENDPOINT_ARG"; fi; \
    if [ ! -z "$JIRA_REDIRECT_LINK_ARG" ]; then export JIRA_REDIRECT_LINK="$JIRA_REDIRECT_LINK_ARG"; fi; \
    if [ ! -z "$JIRA_CLIENT_ID_ARG" ]; then export JIRA_CLIENT_ID="$JIRA_CLIENT_ID_ARG"; fi; \
    if [ ! -z "$JIRA_SECRET_ARG" ]; then export JIRA_SECRET="$JIRA_SECRET_ARG"; fi; \
    if [ ! -z "$GITHUB_CLIENT_ID_ARG" ]; then export GITHUB_CLIENT_ID="$GITHUB_CLIENT_ID_ARG"; fi; \
    if [ ! -z "$GITHUB_SECRET_ARG" ]; then export GITHUB_SECRET="$GITHUB_SECRET_ARG"; fi;

COPY --from=config /app/src/main/resources /app/src/main/resources
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=deployment","/app.jar"]
