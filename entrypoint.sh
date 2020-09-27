#!/bin/bash

cd ${GITHUB_WORKSPACE}

FILENAME=$(git diff-tree -r --name-only --no-commit-id ${GITHUB_SHA} | grep "${INPUT_RELAY_WORKFLOW_FILE}" | head -1)
echo "filename: ${FILENAME}"

if [[ -n ${FILENAME} ]]; then
  echo "${INPUT_RELAY_PASSWORD}" | relay auth login ${INPUT_RELAY_USERNAME} -p
  [[ $? == 0 ]] && relay workflow download ${INPUT_RELAY_WORKFLOW} >/dev/null
  if [[ $? == 0 ]]; then
    relay workflow replace ${INPUT_RELAY_WORKFLOW} -f ${FILENAME}
    relay workflow run ${INPUT_RELAY_WORKFLOW} ${INPUT_RELAY_WORKFLOW_RUN_PARAMETERS}
    exit $?
  else
    echo "no workflow matching ${INPUT_RELAY_WORKFLOW} found, exiting cleanly"
    exit 0
  fi
else
  echo "Could not find a workflow name from git diff-tree at ${GITHUB_SHA}"
  echo "Diff tree was: "
  git diff-tree -r --name-only --no-commit-id ${GITHUB_SHA}
  exit 0
fi
