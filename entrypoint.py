#!/usr/bin/env python

import os
import yaml
# we're doing lots of environment manipulation, so make it easy
from os import environ as env
from subprocess import CalledProcessError, PIPE, STDOUT, run


def configure_cli():
    # translate from github env vars to the ones Relay CLI expects
    if env['INPUT_RELAY_HOST_API']:
        os.putenv("RELAY_API_DOMAIN", env['INPUT_RELAY_HOST_API'])
    if env['INPUT_RELAY_HOST_UI']:
        os.putenv("RELAY_UI_DOMAIN", env['INPUT_RELAY_HOST_UI'])


def setup_workflow(workflow_file, workflow_name):
    # set up the file and workflow name to operate on
    try:
        stat = os.stat(workflow_file)
        with open(workflow_file) as wf_obj:
            workflow_contents = wf_obj.read
    except:
        print("Workflow file specified does not exist:", workflow_file)
        exit(1)

    if len(workflow_name) == 0:
        workflow_name = os.path.basename(workflow_file).split('.')[0]

    return workflow_file, workflow_name, workflow_contents


def do_login():
    try:
        # BUG args should be a sequence but the relay command only sees the first one
        login_command = "relay auth login " + \
            env['INPUT_RELAY_USERNAME'] + " -p"
        login_result = run(login_command, input=env['INPUT_RELAY_PASSWORD'],
                           stderr=STDOUT, stdout=PIPE, check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("Relay login failed: ", e, e.stdout)
        exit(1)


def download_and_replace(workflow_file, workflow_name, workflow_contents):
    # download, compare, update if local version changed
    try:
        download_command = "relay workflow download " + workflow_name
        download_result = run(
            download_command, capture_output=True, check=True, shell=True, text=True)
    except CalledProcessError as e:
        if e.stdout.find("could not find record"):
            add_new_workflow(workflow_file, workflow_name)
            pass

    if workflow_contents != download_result.stdout:
        try:
            replace_command = "relay workflow replace " + \
                workflow_name + " -f " + workflow_file
            replace_result = run(
                replace_command, capture_output=True, check=True, shell=True, text=True)
        except CalledProcessError as e:
            print("Could not replace workflow", e, e.stdout)
            exit(1)


def add_new_workflow(workflow_file, workflow_name):
    try:
        add_command = "relay workflow add " + workflow_name + " -f" + workflow_file
        add_result = run(add_command, capture_output=True,
                         check=True, shell=True, text=True)
    except CalledProcessError as e:
        print("Could not add new workflow", e, e.stdout)
        exit(1)
    print("Added new workflow to your account, view it on the web:", add_result.stdout)
    exit(0)

# we expect config to be a yaml list of maps, each with keys
# - `file` for the filesystem path to its corresponding file in the repo
# - `name` for the service name of the workflow and


def update_workflows():

    mapping_file = 'workflow_mappings.yaml'

    if os.path.exists(mapping_file):
        with open(mapping_file) as config:
            mappings = yaml.load(config, Loader=yaml.FullLoader)

        for entry in mappings:
            workflow_file, workflow_name, workflow_contents = setup_workflow(
                entry['file'], entry['name'])
            download_and_replace(
                workflow_file, workflow_name, workflow_contents)

    else:  # no config file, test for environment vars to operate on one workflow
        workflow_file, workflow_name, workflow_contents = setup_workflow(
            env['INPUT_RELAY_WORKFLOW_FILE'], env['INPUT_RELAY_WORKFLOW'])
        download_and_replace(workflow_file, workflow_name, workflow_contents)


os.chdir(env['GITHUB_WORKSPACE'])

configure_cli()

do_login()

update_workflows()
