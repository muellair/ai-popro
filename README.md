# Welcome to the Platform for AI-based Cyber-Physical Systems

## Getting Started

### Set up docker

### Setup python environment

## Run the application

### Container `aibas-dev`

#### Without VSCode

Create image `aibas-dev`:
    docker build -t aibas-dev -f .devcontainer/Dockerfile .
Run container (Interactive + TTY), with current working directory mounted in the container at `/workspace`:
    docker run -it --rm \
      -v $(pwd):/workspace \
      aibas-dev bash


## Develop

Changes to be persisted in docker images should happen in the Dockerfile as single source of truth: Adapt it and re-build with above commands.


### Tips

#### VSCode Dev Containers:
- at every vscode restart: open project root, `Dev Containers: Rebuild and Reopen in Container`
- container logs: `Dev Containers: Show Container Log`
- in case image `aibas-dev` was created with plain docker commands, cf. https://stackoverflow.com/questions/74217946/how-can-i-use-a-local-image-using-vscode-devcontainer for how to open the already-built image with VSCode