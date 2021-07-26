JAR_PATH="$PWD/build/libs/edu.nd.crc.safa-0.1.0.jar"

(
  set -a &&
    source .env &&
    java -jar "$JAR_PATH"
)
