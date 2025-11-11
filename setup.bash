#!/bin/bash
# shellcheck source=/dev/null

# This script is used to setup a development environment for chandra.
# It will clone the chandra repository, build the docker images and start the container.
# It will also start the docker compose for the specified project if the MY_DOCKER COMPOSE_FILE variable is set.
#
source .env

#
# Function to start the environment
#
function launch_env() {

  if cd "$WORK_DIR"; then
    if ! docker compose build --no-cache \
          --build-arg ROOT_PROJ_DIR="$ROOT_PROJ_DIR"; then
      echo "failed to build the $PROJECT_NAME Docker Image"
      exit 1
    fi
  else
    echo "failed to enter directory '$WORK_DIR'"
    exit 1
  fi

  docker compose -p "$PROJ_NAME" up -d  || {
    echo "failed to start the $PROJECT_NAME Container"
    exit 1
  }

  sleep 5

  docker compose -p "$COMPOSE_PROJ_NAME" -f "tmp/wrapster/docker-compose.yaml" up -d  || {
    echo "failed to start the $REPO_NAME Container"
    exit 1
  }

  sleep 5

  docker exec -itd $CONTAINER_NAME python -m chandra.cli_scripts.stream_consumer || {
      echo "failed to start the consumer"
      exit 1
    }
}

#
# Function to unset the environment variables
#
function unset_env() {

  unset CONTAINER_NAME

}

#
# Function to destroy the environment
#
function destroy_env() {

  cd "$WORK_DIR" || return 1

  if docker compose ls --all | awk '{print $1}' | grep -q "${COMPOSE_PROJ_NAME}"; then
     docker compose -p "${COMPOSE_PROJ_NAME}" down -v
  fi

  if docker compose ls --all | awk '{print $1}' | grep -q "$PROJECT_NAME"; then
     docker compose -p "$PROJECT_NAME" down -v
  fi

}

#
# Variables
#
ROOT_PROJ_DIR="${ROOT_PROJ_DIR:="/app"}"
: "${COMPOSE_PROJ_NAME:="wrapster_project"}"

export CONTAINER_NAME="${CONTAINER_NAME:="${PROJECT_NAME}_container"}"

# Emoji for status
CLONE="⬇️"
CLONE_SUCCESS="⬇️✅"
CLONE_FAILURE="⬇️❌"
PULL="🔄"
PULL_SUCCESS="🔄✅"
PULL_FAILURE="🔄❌"
WORK_DIR="$PWD"


if [[ "$#" -eq 1 && "$1" == "up" ]]; then
  launch_env
  unset_env
elif [[ "$#" -eq 1 && "$1" == "down" ]]; then
  destroy_env
  unset_env
else
  echo "Invalid Input. Try again with up/down/repo"
  exit 1
fi
