#!/bin/bash

cd ${GITHUB_WORKSPACE}

if [[ -n ${INPUT_RELAY_WORKFLOW_FILE} ]]; then
  mkdir -p ~/.config/relay
  if [[ -n ${INPUT_RELAY_HOST_API} ]]; then
    echo 'api_domain: ' ${INPUT_RELAY_HOST_API} >> ~/.config/relay/config.yaml
  fi

  if [[ -n ${INPUT_RELAY_HOST_UI} ]]; then
    echo 'ui_domain: ' ${INPUT_RELAY_HOST_UI} >> ~/.config/relay/config.yaml
  fi

  WORKFLOW=${INPUT_RELAY_WORKFLOW}
  if [[ -z ${WORKFLOW} ]]; then
    FILENAME=$(basename -- "${INPUT_RELAY_WORKFLOW_FILE}")
    WORKFLOW="${FILENAME%.*}"
  fi

  echo "${INPUT_RELAY_PASSWORD}" | relay auth login ${INPUT_RELAY_USERNAME} -p
  [[ $? == 0 ]] && relay workflow download ${WORKFLOW} >/dev/null
  if [[ $? == 0 ]]; then
    relay workflow replace ${WORKFLOW} -f ${INPUT_RELAY_WORKFLOW_FILE}
  else
    relay workflow add ${WORKFLOW} -f ${INPUT_RELAY_WORKFLOW_FILE}
  fi

  if [[ $? == 0 ]]; then
    relay workflow run ${WORKFLOW} ${INPUT_RELAY_WORKFLOW_RUN_PARAMETERS}
  fi
fi
