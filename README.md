# relaysh-docker-action

This github action will update a relay.sh workflow upon commit to a repo.

## Caveats

It has a couple of restrictions, specifically:

- the commit contains no more than one yaml file, which is the workflow to be updated
- the workflow name on the service matches the filename, minus the .yaml extension
- you've set up repo secrets RELAY_USERNAME and RELAY_PASSWORD with your login creds to relay

## Usage

To use it, add a GitHub Actions workflow in the repo where you keep your Relay workflows
(Sorry for the terminology overlap, it's a crowded namespace!).

```yaml
name: update-workflow-on-commit

# Controls when the action will run. Triggers the workflow on push or pull request
# events but only for the master branch
on:
  push:
    branches: [ main ]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
    # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
    - uses: actions/checkout@v2
      with:
        fetch-depth: 0
    - uses: ahpook/relaysh-docker-update-workflow@master
      with:
        RELAY_USERNAME: ${{ secrets.RELAY_USERNAME }}
        RELAY_PASSWORD: ${{ secrets.RELAY_PASSWORD }}
```
