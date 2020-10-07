# relaysh-docker-action

This github action will update and run a relay.sh workflow upon commit to a repo.

## Usage

To use it, add a GitHub Actions workflow in the repo where you keep your Relay workflows.

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
        RELAY_USERNAME: ${{ secrets.RELAY_USERNAME }}
        RELAY_PASSWORD: ${{ secrets.RELAY_PASSWORD }}
        # OPTIONAL: see workflow_mappings section below
        RELAY_WORKFLOW: "relay-workflow-name"
        RELAY_WORKFLOW_FILE: "relay.yaml"
        # OPTIONAL: enables pointing the relay CLI at the local dev environment
        RELAY_HOST_API: "api.relay.sh"
        RELAY_HOST_UI: "ui.relay.sh"
```

The action's behavior is configurable based on the presence of a `workflow_mappings.yaml` configuration file in the root of the repository. This file's purpose is to map filenames inside the repository to workflow names as they exist on the Relay service. As such, it should be a list of maps, each with a `name` and `file` key, where `name` is the user-visible workflow name on the Relay service (i.e. displayed by `relay workflow list`) and `file` is the path and filename of the workflow YAML, relative to the repository root. See the [workflow_mappings.yaml](workflow_mappings.yaml) in this directory for an example.
