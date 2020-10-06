#!/usr/bin/env python

import os
# we're doing lots of environment manipulation, so make it easy
from os import environ as env
from subprocess import CalledProcessError, PIPE, STDOUT, run

os.chdir(env['GITHUB_WORKSPACE'])

# set up configuration if needed
if env['INPUT_RELAY_HOST_API'] or env['INPUT_RELAY_HOST_UI']:
  configpath = env['HOME'] + "/.relay/"
  configfile = configpath + "config.yaml"
  try: 
    os.makedirs(configpath)
  except FileExistsError:
    pass

  with open(configfile,'a') as configfd:
    if env['INPUT_RELAY_HOST_API']: 
      configfd.write("api_domain: " + env['INPUT_RELAY_HOST_API'] + "\n")
    if env['INPUT_RELAY_HOST_UI']:
      configfd.write("ui_domain: " + env['INPUT_RELAY_HOST_UI'] + "\n")

# set up the file and workflow name to operate on
workflow_file = env['INPUT_RELAY_WORKFLOW_FILE']
try:
  stat = os.stat(workflow_file)
  with open(workflow_file) as wf_obj:
    local_workflow_contents = wf_obj.read
except:
  print("Workflow file specified does not exist:", workflow_file)
  exit(1)

workflow = env['INPUT_RELAY_WORKFLOW']
if len(workflow) == 0:
  workflow = os.path.basename(workflow_file).split('.')[0]

# login sequence (TODO make this a function)
try:
  # this should be a sequence but the relay command only sees the first arg
  login_command = "relay auth login " + env['INPUT_RELAY_USERNAME'] + " -p"
  login_result = run(
    login_command,
    input=env['INPUT_RELAY_PASSWORD'],
    stderr=STDOUT,
    stdout=PIPE,
    check=True,
    shell=True,
    text=True)
except CalledProcessError as e:
  print("Relay login failed: ", e, e.stdout)
  exit(1)

# download, compare, update if local version changed
try:
  download_command = "relay workflow download " + workflow
  download_result = run(
    download_command,
    capture_output=True,
    check=True,
    shell=True,
    text=True)
except CalledProcessError as e:
  if e.stdout.find("could not find record"):
    # todo this should run a method to 'relay workflow add' it
    pass

if local_workflow_contents != download_result.stdout:
  try:
    replace_command = "relay workflow replace " + workflow + " -f " + workflow_file
    replace_result = run(
      replace_command,
      capture_output=True,
      check=True,
      shell=True,
      text=True
    )
  except CalledProcessError as e:
    print("Could not replace workflow", e, e.stdout)
    exit(1)