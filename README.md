# relaysh-docker-action

This GitHub Action will update and run a [Relay](https://relay.sh) workflow upon commit to a repository.

## Usage

To use it, add a GitHub Actions workflow in the repository where you keep your Relay workflows.

```yaml
name: update-and-run-workflow-on-commit

on:
  push:
    branches: [ main ]

  update:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - uses: puppetlabs/relaysh-docker-update-workflow@main
      with:
        RELAY_API_TOKEN: ${{ secrets.RELAY_API_TOKEN }}
        RELAY_WORKFLOW: "relay-workflow-name"
        RELAY_WORKFLOW_FILE: "relay.yaml"
```

The action's behavior is configurable based on the presence of a `workflow_mappings.yaml` configuration file in the root of the repository. This file's purpose is to map filenames inside the repository to workflow names as they exist in Relay. As such, it should be a list of maps, each with a `name` and `file` key, where `name` is the user-visible workflow name in Relay (i.e. displayed by `relay workflow list`) and `file` is the path and filename of the workflow YAML, relative to the repository root. See the [workflow_mappings.yaml](workflow_mappings.yaml) in this directory for an example.
