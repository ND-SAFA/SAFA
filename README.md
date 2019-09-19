# SAFA Services API

## Requirements
JDK 1.8\
Gradle 4+\
neo4j (or docker)

## Dev Setup 
```bash
docker pull neo4j
```

```bash
docker run -d --name neo4j \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=neo4j_data:/data \
    --env=NEO4J_AUTH=none \
    neo4j
```

Reset neo4j password:
```bash
curl -v -u neo4j:neo4j -X POST localhost:7474/user/neo4j/password -H "Content-type:application/json" -d "{\"password\":\"secret\"}"
```

## Build and Run

```bash
./gradlew clean build && java -jar build/libs/*jar
```

Should serve on localhost:8080

## Reference Documentation
For further reference, please consider the following sections:

* [Official Gradle documentation](https://docs.gradle.org)
* [Spring Boot Gradle Plugin Reference Guide](https://docs.spring.io/spring-boot/docs/2.1.8.RELEASE/gradle-plugin/reference/html/)
* [Spring Boot DevTools](https://docs.spring.io/spring-boot/docs/{bootVersion}/reference/htmlsingle/#using-boot-devtools)

### Additional Links
These additional references should also help you:

* [Gradle Build Scans – insights for your project's build](https://scans.gradle.com#gradle)

