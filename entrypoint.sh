#!/bin/bash

cd ${GITHUB_WORKSPACE}
FILENAME=$(git diff-tree -r --name-only --no-commit-id ${GITHUB_SHA} | grep yaml | head -1)

if [[ -n ${FILENAME} ]]; then
  WORKFLOW=$(basename ${FILENAME} .yaml)
  echo "${INPUT_RELAY_PASSWORD}" | relay auth login ${INPUT_RELAY_USERNAME} -p
  relay workflow replace ${WORKFLOW} -f ${FILENAME}
else
  echo "Could not determine filename from git diff-tree at ${GITHUB_SHA}"
  exit 1
fi
