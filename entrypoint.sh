#!/bin/bash

cd ${GITHUB_WORKSPACE}

if [[ -n ${INPUT_RELAY_WORKFLOW_FILE} ]]; then
  echo "${INPUT_RELAY_PASSWORD}" | relay auth login ${INPUT_RELAY_USERNAME} -p
  [[ $? == 0 ]] && relay workflow download ${INPUT_RELAY_WORKFLOW} >/dev/null
  if [[ $? == 0 ]]; then
    relay workflow replace ${INPUT_RELAY_WORKFLOW} -f ${INPUT_RELAY_WORKFLOW_FILE}
    relay workflow run ${INPUT_RELAY_WORKFLOW} ${INPUT_RELAY_WORKFLOW_RUN_PARAMETERS}
    exit $?
  else
    echo "no workflow matching ${INPUT_RELAY_WORKFLOW} found, exiting cleanly"
    exit 0
  fi
fi
