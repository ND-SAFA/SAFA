FROM gradle:5.6.2-jdk8 AS builder
COPY checkstyle.xml /app/checkstyle.xml
WORKDIR /app
ADD build.gradle /app/
ADD src/ /app/src/
RUN sed -i s/neo4j.host=localhost/neo4j.host=neo4j/ /app/src/main/resources/application.properties && \
    sed -i s/mysql.host=localhost/mysql.host=$_MY_SQL_HOST/ /app/src/main/resources/application.properties && \
    sed -i s/mysql.username=user/mysql.username=$_MY_SQL_USERNAME/ /app/src/main/resources/application.properties && \
    sed -i s/mysql.password=secret3/mysql.password=$_MY_SQL_PASSWORD/ /app/src/main/resources/application.properties && \
    gradle build --stacktrace

FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
