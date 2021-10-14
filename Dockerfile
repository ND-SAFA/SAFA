FROM gradle:6.9-jdk11 AS builder

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD resources/ /app/resources/

WORKDIR /app
RUN gradle build --stacktrace

FROM openjdk:11
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar","-Dspring.profiles.active=prod", "/app.jar"]
