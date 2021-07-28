#!/usr/bin/env python

import os
import yaml
from os import environ
from shlex import join, quote
from subprocess import CalledProcessError, PIPE, STDOUT, run

cli_args = []

config = environ['INPUT_RELAY_CONFIGURATION_FILE']
if config:
    cli_args.extend(["--config", quote(config)])

context = environ['INPUT_RELAY_CONFIGURATION_CONTEXT']
if context:
    cli_args.extend(["--context", quote(context)])

debug = environ['INPUT_RELAY_CONFIGURATION_DEBUG']
if debug:
    cli_args.append("--debug")


def do_login():
    try:
        login_command = ["relay", "auth", "login", "--stdin"]
        login_command.extend(cli_args)
        run(join(login_command), input=environ['INPUT_RELAY_API_TOKEN'],
            stderr=STDOUT, stdout=PIPE, check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("relay auth login failed: ", e, e.stdout)
        exit(1)


def save_workflow(workflow_file, workflow_name):
    try:
        if len(workflow_name) == 0:
            workflow_name = os.path.basename(workflow_file).split('.')[0]

        save_workflow_command = ["relay", "workflow", "save",
                                 quote(workflow_name), "-f", quote(workflow_file)]
        save_workflow_command.extend(cli_args)
        run(join(save_workflow_command), capture_output=True,
            check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("relay workflow save failed: ", e, e.stdout)
        exit(1)


def update_workflows():

    # we expect config to be a yaml list of maps, each with keys
    # - `file` for the filesystem path to its corresponding file in the repo
    # - `name` for the service name of the workflow and
    mapping_file = 'workflow_mappings.yaml'

    if os.path.exists(mapping_file):
        with open(mapping_file) as config:
            mappings = yaml.load(config, Loader=yaml.FullLoader)

        for entry in mappings:
            save_workflow(entry['file'], entry['name'])

    else:
        save_workflow(environ['INPUT_RELAY_WORKFLOW_FILE'],
                      environ['INPUT_RELAY_WORKFLOW'])


os.chdir(environ['GITHUB_WORKSPACE'])

do_login()

update_workflows()
