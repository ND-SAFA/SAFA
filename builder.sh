runDev(){
  setGoogleCredentials
  runServer safa-dev
}

runProd(){
  setGoogleCredentials
  runServer safa-prod
}

runLocalWithCredentials(){
  setGoogleCredentials
  runLocal
}

setGoogleCredentials(){
    export GOOGLE_APPLICATION_CREDENTIALS="$PWD/application-credentials.json"
}

runLocal() {
  runServer dev
}

buildNoTests() {
  (
    ./gradlew build --stacktrace -x Test -x checkstyleMain -x checkstyleTest
  )
}

buildWithTests() {
  (
    ./gradlew build --stacktrace
  )
}

build(){
  if [ $1 == "test" ]; then
    buildWithTests
  else
    buildNoTests
  fi
}

runServer(){
    JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

  (
          java -jar -Dspring.profiles.active="$1" "$JAR_PATH"
      )
}

# Checks that valid command was given
for command in "build" "buildrun"; do
    if [ -z "$1" ]
      then
        echo "Please choose a comment: build, buildrun"
        exit
    fi
  done

if [ -z "$2" ]
  then
    echo "Please choose an environment: local, dev, prod"
    exit
fi

if [ -z "$3" ]
  then
    echo "Please choose an environment: test, no-test"
    exit
fi

if [ $1 == "build" ]; then
  build "test"
fi

if [ $2 == "local" ]; then
  build $3 && runLocal
fi

if [ $2 == "local-creds" ]; then
  build $3 && runLocalWithCredentials
fi

if [ $2 == "dev" ]; then
  build $3 && runDev
fi

if [ $2 == "prod" ]; then
  build $3 && runProd
fi
