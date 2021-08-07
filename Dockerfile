FROM gradle:6.9.0-jdk8 AS builder

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/

WORKDIR /app
RUN gradle build --stacktrace

FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
