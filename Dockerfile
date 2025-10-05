# Step 1 - Install necessary dependencies
FROM public.ecr.aws/amazoncorretto/amazoncorretto:17 AS builder
SHELL ["/bin/bash", "-c"]

# Step 2 - Install gradle
ARG GRADLE_VERSION=8.1
RUN yum update -y -q && yum install -y -q wget unzip zip tar
RUN curl -q -s "https://get.sdkman.io" | bash
RUN source "$HOME/.sdkman/bin/sdkman-init.sh" && sdk install gradle $GRADLE_VERSION

# Step 3 - Install deps
WORKDIR /app
ADD builder.sh .
ADD build.gradle .
ADD settings.gradle .
ADD gradlew .
ADD gradle gradle
RUN chmod +x gradlew
RUN ./gradlew --no-daemon dependencies

# Step 3 - Copy source code
ARG PathToProperties="/app/src/main/resources/application-deployment.properties"
ADD src/main/resources src/main/resources
ADD src/main/java src/main/java
ADD src/test src/test

# Step 4 - Install gradle version for building

RUN ./gradlew build --stacktrace -x Test -x checkstyleMain -x checkstyleTest

## Step - Create endpoint
ENV RUN_SCRIPT="/app/run.sh"
ARG JAR_PATH="/app.jar"
ARG SPRING_PROFILE=deployment
RUN \
    mkdir -p "$(dirname $RUN_SCRIPT)"; \
    touch "$RUN_SCRIPT"; \
    chmod +x "$RUN_SCRIPT"; \
    echo "java -Djava.security.egd=file:/dev/./urandom -jar -Dspring.profiles.active=${SPRING_PROFILE} ${JAR_PATH}" >> "$RUN_SCRIPT"; \
    cat "$RUN_SCRIPT"

ENV PORT=80
RUN mv "$(/app/builder.sh print_path)" $JAR_PATH
ENTRYPOINT /bin/bash $RUN_SCRIPT
