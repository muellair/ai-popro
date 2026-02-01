# Welcome to the Platform for AI-based Cyber-Physical Systems

This project was created by Jonathan Kinkel and Felix Müller as part of the course  
**“M. Grum: Advanced AI-based Application Systems”**  
held by the **Junior Chair for Business Information Science, esp. AI-based Application Systems**  
at the **University of Potsdam**.

In this project, we developed an ANN model predicting the yearly evolution of population of the German federal states. As a baseline, we include an OLS model fitted for the same task.


## Model performance indicators

Model performance indicators can be found in `artifacts`. Further insights into data, like diagnostic plots, are gathered in `data_visualization/output/`.


## Using the application

### Set up docker

Please refer to the [docker documentation](https://docs.docker.com/get-started/).
For developing purposes, including reproducing training and fitting of models, please use the environment provided in `.devcontainer` (cf. section (Development)[##development] below).

### Run the application

From the project's root directory, run:
```
docker volume create ai_system

docker compose -f scenarios/neural-network/docker-compose-ai.yaml up
docker compose -f scenarios/ordinary-least-squares/docker-compose-ols.yaml up
```

While explicit `docker pull` commands should not be needed, they would be:
```
docker pull muellairnot00/knowledgebase_aipopro
docker pull muellairnot00/activationbase_aipopro
docker pull muellairnot00/codebase_aipopro
```


### Stop the application

Once again from the project's root directory, run:

```
docker-compose -f scenarios/neural-network/docker-compose-ai.yaml down
docker-compose -f scenarios/neural-network/docker-compose-ols.yaml down
docker volume rm ai_system
```

## Development

To reproduce the training of the ANN and the fitting of the OLS model, create a Docker container `aibas-dev`. It will contain all the needed python installation and dependencies. Please refer to the [VSCode documentation](https://code.visualstudio.com/docs/devcontainers/containers) for developing in docker containers with VSCode.
1) Create image
`aibas-dev`:
    `docker build -t aibas-dev -f .devcontainer/Dockerfile .`
3) Run container (Interactive + TTY), with current working directory mounted in the container at
`/workspace`:
    `docker run -it --rm -v $(pwd):/workspace aibas-dev bash`

Changes to be persisted in docker images should happen in the Dockerfile as single source of truth: Adapt it and re-build with above commands.

For re-building the docker images, run in from the root directory:
```
docker build -t muellairnot00/knowledgebase_aipopro -f images/knowledgeBase_aipopro/Dockerfile .
docker build -t muellairnot00/learningbase_aipopro -f images/learningBase_aipopro/Dockerfile .
docker build -t muellairnot00/activationbase_aipopro -f images/activationBase_aipopro/Dockerfile .
docker build -t muellairnot00/codebase_aipopro -f images/codeBase_aipopro/Dockerfile .
```


## References and credits

The dataset was obtained from the German Federal Statistical Office (Destatis),
table **12411-0010 – Population: Federal States**, via the GENESIS online system (https://www-genesis.destatis.de/datenbank/online/table/12411-0010/table-toolbar).

The shapefile used for visualization purposes:
© BKG (Jahr des letzten Datenbezugs) dl-de/by-2-0, Datenquellen: https://sgx.geodatenzentrum.de/web_public/gdz/datenquellen/datenquellen_vg_nuts.pdf


## Models
- Neural Network: TensorFlow/Keras
- Linear Baseline: OLS regression using Statsmodels

Both models are trained and evaluated on identical data splits.


## Repository structure

```
├── artifacts
│   ├── evaluation_summary.txt
│   └── train_val_loss.png
├── CITATION.cff
├── data
│   ├── preprocessed
│   │   ├── activation_data.csv
│   │    ...
│   ├── raw
│   │   └── population_raw.csv
│   └── shapefile_states_ger
│       ├── nuts250_1231
│       │   ├── NUTS250_N1.cpg
│       │   ...
│        ...
├── data_visualization
│   ├── data_vis.py
│   ├── diagnosticPlots.py
│   ├── __init__.py
│   └── output
│       ├── diagnostic_plots.png
│       ...
│       └── scatterplots
│           ├── Bayern_population_over_years.png
│           ...
├── .devcontainer
│   ├── devcontainer.json
│   └── Dockerfile
├── .gitignore
├── images
│   ├── activationBase_aipopro
│   │   ├── Dockerfile
│   │   └── Readme.md
│   ...
├── __init__.py
├── learningBase
│   ├── currentAiSolution.keras
│   └── currentOlsSolution.pkl
├── LICENSE
├── notebooks
│   └── preprocess.ipynb
├── README.md
├── requirements.txt
├── scenarios
│   ├── neural-network
│   │   └── docker-compose-ai.yaml
│   └── ordinary-least-squares
│       └── docker-compose-ols.yaml
└── src
    ├── evaluate.py
    ├── __init__.py
    ├── preprocess.py
    ├── scrape.py
    ├── train_nn.py
    └── train_ols.py
```

## License
This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.


