build() {
  (
    sed 's,jdbc:mysql://localhost/safa-db,jdbc:h2:mem:safa-db/,g' ".env" >test.env &&
      ./gradlew build --stacktrace # automatically reads env files
  )
  echo "DONE"
  rm test.env
}

run() {
  JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

  (
    set -a &&
      source .env &&
      java -jar "$JAR_PATH"
  )
}

if [ $1 == "build" ]; then
  build
fi

if [ $1 == "run" ]; then
  run
fi

if [ $1 == "buildrun" ]; then
  build
  run
fi
