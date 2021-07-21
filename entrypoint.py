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


def setup_workflow(workflow_file, workflow_name):
    try:
        with open(workflow_file) as wf_obj:
            workflow_contents = wf_obj.read
    except IOError:
        print("Workflow file specified does not exist:", workflow_file)
        exit(1)

    if len(workflow_name) == 0:
        workflow_name = os.path.basename(workflow_file).split('.')[0]

    return workflow_file, workflow_name, workflow_contents


def do_login():
    try:
        login_command = ["relay", "auth", "login", "--stdin"]
        login_command.extend(cli_args)
        run(join(login_command), input=environ['INPUT_RELAY_API_TOKEN'],
            stderr=STDOUT, stdout=PIPE, check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("Relay login failed: ", e, e.stdout)
        exit(1)


def download_and_replace(workflow_file, workflow_name, workflow_contents):
    try:
        download_command = ["relay", "workflow",
                            "download", quote(workflow_name)]
        download_command.extend(cli_args)
        download_result = run(
            join(download_command), capture_output=True, check=True, shell=True, text=True)
    except CalledProcessError as e:
        if e.stdout.find("could not find record"):
            add_new_workflow(workflow_file, workflow_name)

    if workflow_contents != download_result.stdout:
        try:
            replace_command = ["relay", "workflow", "replace",
                               quote(workflow_name), "-f", quote(workflow_file)]
            replace_command.extend(cli_args)
            run(join(replace_command), capture_output=True,
                check=True, shell=True, text=True)
        except CalledProcessError as e:
            print("Could not replace workflow", e, e.stdout)
            exit(1)


def add_new_workflow(workflow_file, workflow_name):
    try:
        add_command = ["relay", "workflow", "add",
                       quote(workflow_name), "-f", quote(workflow_file)]
        add_command.extend(cli_args)
        add_result = run(join(add_command), capture_output=True,
                         check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("Could not add new workflow", e, e.stdout)
        exit(1)
    print("Added new workflow to your account, view it on the web:", add_result.stdout)
    exit(0)


def update_workflows():

    # we expect config to be a yaml list of maps, each with keys
    # - `file` for the filesystem path to its corresponding file in the repo
    # - `name` for the service name of the workflow and
    mapping_file = 'workflow_mappings.yaml'

    if os.path.exists(mapping_file):
        with open(mapping_file) as config:
            mappings = yaml.load(config, Loader=yaml.FullLoader)

        for entry in mappings:
            workflow_file, workflow_name, workflow_contents = setup_workflow(
                entry['file'], entry['name'])
            download_and_replace(
                workflow_file, workflow_name, workflow_contents)

    else:
        workflow_file, workflow_name, workflow_contents = setup_workflow(
            environ['INPUT_RELAY_WORKFLOW_FILE'], environ['INPUT_RELAY_WORKFLOW'])
        download_and_replace(workflow_file, workflow_name, workflow_contents)


os.chdir(environ['GITHUB_WORKSPACE'])

do_login()

update_workflows()
