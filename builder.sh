#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

JAR_PATH="$SCRIPT_DIR/build/libs/edu.nd.crc.safa-0.1.0.jar"

HELP_TEXT="
Usage: builder.sh [options] <command>...

Options:
      -h    Display this message.
      -n    Do not run unit tests. Overrides a previous -t. Ignored if
            'build' is not one of the commands.
      -t    Run unit tests (this is the default behavior if building).
            Overrides a previous -n. Ignored if 'build' is not one of the
            commands.
      -e    Specify the environment (local, dev, or prod). If not specified,
            it defaults to local.

Commands:
      build    Build the backend with Gradle
      run      Run the backend
"

function help {
  echo "$HELP_TEXT"

  if [ -z "$1" ]; then
    exit 0
  else
    exit "$1"
  fi
}

function setGoogleCredentials {
    export GOOGLE_APPLICATION_CREDENTIALS="$SCRIPT_DIR/application-credentials.json"
}

function build {
  # Set up args for testing
  if $1; then
    TEST_ARGS=""
  else
    TEST_ARGS="-x Test -x checkstyleMain -x checkstyleTest"
  fi

  # shellcheck disable=SC2086
  "$SCRIPT_DIR/gradlew" build --stacktrace $TEST_ARGS
  return $?
}

function run {
  java -jar -Dspring.profiles.active="$1" "$JAR_PATH"
  return $?
}

function checkReturn {
  if [ "$1" -ne 0 ]; then
    exit "$1"
  fi
}

# Parse arguments
TEST=true
ENVIRONMENT=local
BUILD=false
RUN=false
while [ $OPTIND -le "$#" ]; do
  if getopts ':hnte:' option; then
    case $option in
      h) help;;
      n) TEST=false;;
      t) TEST=true;;
      e) ENVIRONMENT="$OPTARG";;
      :) echo -e "option requires an argument."; help 1;;
      ?) echo -e "Invalid command option."; help 1;;
    esac
  else
    command="${!OPTIND}"
    ((OPTIND++))

    case $command in
      build) BUILD=true;;
      run) RUN=true;;
      *) echo -e "Unknown command $command"; help 1;;
    esac
  fi
done

# Check that the environment is valid and translate the name
case $ENVIRONMENT in
  local) ENVIRONMENT=dev;;
  dev) ENVIRONMENT=safa-dev;;
  prod) ENVIRONMENT=safa-prod;;
  *) echo -e "Unknown environment $ENVIRONMENT"; help 1;;
esac

# Check the user gave us something to do
if [[ $BUILD = false && $RUN = false ]]; then
  echo -e "No command specified."
  help 1
fi

if $BUILD; then
  build $TEST
  checkReturn $?
fi

if $RUN; then
  run $ENVIRONMENT
  checkReturn $?
fi
