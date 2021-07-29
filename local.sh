build() {
  (
    set -a &&
      source .env &&
      ./gradlew build --stacktrace # automatically reads env files
  )
}

run() {
  JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

  (
    sed 's,h2:mem:,mysql://localhost/,g' ".env" >test.env &&
      set -a &&
      source test.env &&
      env &&
      java -jar "$JAR_PATH"
  )
  rm test.env
}

if [ $1 == "build" ]; then
  build
fi

if [ $1 == "run" ]; then
  run
fi

if [ $1 == "buildrun" ]; then
  build && run
fi
