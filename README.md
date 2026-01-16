# Welcome to the Platform for AI-based Cyber-Physical Systems

## Getting Started

### Set up docker

### Setup python environment

## Run the application

```
docker volume create ai_system

docker build -t knowledgebase_aipopro images/knowledgeBase_aipopro
docker build -t activationbase_aipopro images/activationBase_aipopro
docker build -t codebase_aipopro images/codeBase_aipopro

docker compose -f docker-compose-ai.yml up
docker compose -f docker-compose-ols.yml up
```


### Container `aibas-dev`

#### Without VSCode
Create image `aibas-dev`:
    `docker build -t aibas-dev -f .devcontainer/Dockerfile .`
Run container (Interactive + TTY), with current working directory mounted in the container at `/workspace`:
    `docker run -it --rm -v $(pwd):/workspace aibas-dev bash`


## Develop

Changes to be persisted in docker images should happen in the Dockerfile as single source of truth: Adapt it and re-build with above commands.


### Tips

#### VSCode Dev Containers:
- at every vscode restart: open project root, `Dev Containers: Rebuild and Reopen in Container`
- container logs: `Dev Containers: Show Container Log`
- in case image `aibas-dev` was created with plain docker commands, cf. https://stackoverflow.com/questions/74217946/how-can-i-use-a-local-image-using-vscode-devcontainer for how to open the already-built image with VSCode

### References and credits
The shapefile used for visualization purposes:
© BKG (Jahr des letzten Datenbezugs) dl-de/by-2-0, Datenquellen: https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf



## Data Origin
The dataset was obtained from the German Federal Statistical Office (Destatis),
table **12411-0010 – Population: Federal States**, via the GENESIS online system.

© Statistisches Bundesamt (Destatis)

## Models
- Neural Network: TensorFlow/Keras
- Linear Baseline: OLS regression using Statsmodels

Both models are trained and evaluated on identical data splits.


## Repository structure (as assumd by Dockerfiles/docker-compose.yml)

```
/tmp/
 ├── knowledgeBase/
 │    ├── currentAiSolution.keras
 │    ├── currentOlsSolution.pkl
 │    └── README.md
 ├── activationBase/
 │    ├── activation_data.csv
 │    └── README.md
 └── codeBase/
      ├── evaluate.py
      └── README.md
```


## Ownership
This repository was created by Jonathan Kinkel and Felix Müller.

## Course Context
This project was created as part of the course  
**“M. Grum: Advanced AI-based Application Systems”**  
held by the **Junior Chair for Business Information Science, esp. AI-based Application Systems**  
at the **University of Potsdam**.

## License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.


