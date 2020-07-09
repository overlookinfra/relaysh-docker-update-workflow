#!/bin/bash

workflow_name=$INPUT_WORKFLOW_NAME
repo_name=$INPUT_REPO_NAME
workflow_path=$INPUT_WORKFLOW_PATH
username=$RELAY_USERNAME
password=$RELAY_PASSWORD

echo "$password" | relay auth login $username -p
relay workflow update $workflow_name -f $workflow_path
