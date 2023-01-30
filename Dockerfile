# Step 1 - Create production environment
FROM ubuntu:12.04 as config
ADD src/main/resources /app/src/main/resources
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"

ARG DB_INSTANCE

ENV DB_URL=jdbc:mysql://host.docker.internal/safa-db
ENV DB_USER=root
ENV DB_PASSWORD=secret2
ENV JWT_KEY=3s6v9y$B&E)H@MbQeThWmZq4t7w!z%C*F-JaNdRfUjXn2r5u8x/A?D(G+KbPeShV
ENV TGEN_ENDPOINT=http://35.184.232.43
ENV JIRA_REDIRECT_LINK="https://localhost.safa.ai:8080/create?tab=jira"
ENV JIRA_CLIENT_ID="lWzIreg3PMSqkjkkvKyqR6xvHJDXvRAF"
ENV JIRA_SECRET="YhfXF-mR0-ZZoH1RD0T504nAfAB002dNVmsmd-JES3LL3_X6kvebRUWh3Ja0IgdT"
ENV GITHUB_CLIENT_ID="Iv1.75905e8f5ace1f4b"
ENV GITHUB_SECRET="2d6bd433619bebf523cef951bd1296ac2d2795c3"

RUN test -n "$DB_URL"
RUN test -n "$DB_USER"
RUN test -n "$DB_PASSWORD"
RUN test -n "$JWT_KEY"
RUN test -n "$TGEN_ENDPOINT"
RUN test -n "$JIRA_REDIRECT_LINK"
RUN test -n "$JIRA_CLIENT_ID"
RUN test -n "$JIRA_SECRET"
RUN test -n "$GITHUB_CLIENT_ID"
RUN test -n "$GITHUB_SECRET"

RUN if [ ! -z "$DB_INSTANCE" ] ; \
    then \
      echo "spring.datasource.hikari.data-source-properties.cloudSqlInstance=$DB_INSTANCE" >> $PathToProperties && \
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
COPY --from=config /app/src/main/resources /app/src/main/resources
COPY --from=builder /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "-Dspring.profiles.active=deployment","/app.jar"]
