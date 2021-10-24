buildNoTests() {
  (
    ./gradlew build --stacktrace -x Test
  )
}

build() {
  (
    ./gradlew build --stacktrace
  )
}

run() {
  JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

  (
      java -jar -Dspring.profiles.active=dev "$JAR_PATH" --debug
  )
}

if [ $1 == "build" ]; then
  build
fi

if [ $1 == "buildrun-no-tests" ]; then
  buildNoTests && run
fi

if [ $1 == "run" ]; then
  run
fi

if [ $1 == "buildrun" ]; then
  build && run
fi
