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
        RELAY_WORKFLOW: "relay-workflow-name"
        RELAY_WORKFLOW_FILE: "relay.yaml"
```
