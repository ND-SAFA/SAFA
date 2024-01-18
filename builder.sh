#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

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
      -f    Specifies an environment file to source before commands.

Commands:
      build          Build the backend with Gradle
      run            Run the backend
      clean          Run a gradle clean
      print_path     Print the path to where the jar will be built based on build.gradle.
                     No other commands will be run even if they are supplied.
      print_version  Print the version of the app based on the contents of build.gradle.
                     No other commands will be run even if they are supplied.
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
  "$SCRIPT_DIR/gradlew" build $TEST_ARGS
  return $?
}

function clean {
  "$SCRIPT_DIR/gradlew" clean
  return $?
}

function run {
  setGoogleCredentials
  if [ -n "$2" ]; then
    echo "Running with environment: $2"
    source "$2"
  fi

  java -jar -Dspring.profiles.active="$1" "$(getJarPath)"
  return $?
}

function checkReturn {
  if [ "$1" -ne 0 ]; then
    exit "$1"
  fi
}

function getBuildVariable {
  awk -F= "/$1/"'{gsub(/^[ \t]*'\''?/,"",$2); gsub(/'\''?[ \t]*$/,"",$2); print $2}' "${SCRIPT_DIR}"/build.gradle
}

function getVersion {
  getBuildVariable archiveVersion
}

function getArchiveBaseName {
  getBuildVariable archivesBaseName
}

function getJarPath {
  echo "$SCRIPT_DIR/build/libs/$(getArchiveBaseName)-$(getVersion).jar"
}

# Parse arguments
TEST=true
ENV_PROPERTIES=local
ENV_FILE=""
BUILD=false
RUN=false
CLEAN=false
while [ $OPTIND -le "$#" ]; do
  if getopts ':hntef:' option; then
    case $option in
      h) help;;
      n) TEST=false;;
      t) TEST=true;;
      e) ENV_PROPERTIES="$OPTARG";;
      f) ENV_FILE="$OPTARG";;
      :) echo -e "option requires an argument."; help 1;;
      ?) echo -e "Invalid command option."; help 1;;
    esac
  else
    command="${!OPTIND}"
    ((OPTIND++))

    case $command in
      build) BUILD=true;;
      run) RUN=true;;
      clean) CLEAN=true;;
      print_path) getJarPath; exit 0;;
      print_version) getVersion; exit 0;;
      *) echo -e "Unknown command $command"; help 1;;
    esac
  fi
done

# Check that the environment is valid and translate the name
case $ENV_PROPERTIES in
  local) ENV_PROPERTIES=dev;;
  dev) ENV_PROPERTIES=safa-dev;;
  prod) ENV_PROPERTIES=safa-prod;;
  *) echo -e "Unknown environment $ENV_PROPERTIES"; help 1;;
esac

# Check the user gave us something to do
if [[ $BUILD = false && $RUN = false && $CLEAN = false ]]; then
  echo -e "No command specified."
  help 1
fi

if $CLEAN; then
  clean
  checkReturn $?
fi

if $BUILD; then
  build $TEST
  checkReturn $?
fi

if $RUN; then
  run $ENV_PROPERTIES $ENV_FILE
  checkReturn $?
fi
