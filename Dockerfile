FROM gradle:5.6.2-jdk8 AS builder
WORKDIR /app
ADD build.gradle /app/
ADD src/ /app/src/
RUN sed -i s/localhost/neo4j/ /app/src/main/resources/application.properties && gradle build

FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]