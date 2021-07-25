JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

(
  sed 's,jdbc:mysql://localhost/safa-db,jdbc:h2:mem:safa-db/,g' ".env" >test.env &&
    set -a &&
    source test.env &&
    ./gradlew build --stacktrace &&
    java -jar "$JAR_PATH"
)
rm test.env
