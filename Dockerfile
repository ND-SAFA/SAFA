FROM gradle:5.6.2-jdk8 AS builder

ADD build.gradle /app/
ADD src/ /app/src/
ADD checkstyle.xml /app/
ADD .env /app/
ADD local-build.sh /app/

WORKDIR /app
RUN sed 's,jdbc:mysql://localhost/safa-db,jdbc:h2:mem:safa-db/,g' ".env" > .env && gradle build -x test


FROM openjdk:8-jdk-alpine
COPY --from=0 /app/build/libs/edu.nd.crc.safa-0.1.0.jar /app.jar
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]
