#!/bin/bash

cd ${GITHUB_WORKSPACE}

FILENAME=$(git diff-tree -r --name-only --no-commit-id ${GITHUB_SHA} | grep "${INPUT_RELAY_WORKFLOWDIR}/.*yaml" | head -1)
echo "filename: ${FILENAME}"

if [[ -n ${FILENAME} ]]; then
  WORKFLOW=$(basename ${FILENAME} .yaml)
  echo "${INPUT_RELAY_PASSWORD}" | relay auth login ${INPUT_RELAY_USERNAME} -p
  [[ $? == 0 ]] && relay workflow get ${WORKFLOW} >/dev/null
  if [[ $? == 0 ]]; then 
    relay workflow replace ${WORKFLOW} -f ${FILENAME}
    exit $?
  else
    echo "no workflow matching ${FILENAME} found, exiting cleanly"
    exit 0
  fi
else
  echo "Could not determine filename from git diff-tree at ${GITHUB_SHA}"
  echo "Diff tree was: "
  git diff-tree -r --name-only --no-commit-id ${GITHUB_SHA}
  exit 1
fi
