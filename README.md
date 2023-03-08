# datasette_etl_workflow_example
This repo is a POC of an ETL that will use datasette as a final destination.

## How to run locally

### Requirements

- Python 3.10
- Docker
- Docker-compose

### Runing the ETL locally

#### Using docker compose

```bash
docker compose build && docker compose up
```

#### Executing the scripts

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Run the datasette server

#### Using docker compose

```bash
docker compose build && docker compose up
```

#### Using datasette cli

```bash
datasette serve --cors --host 
```


## How to run the pipe in github actions


## How to run in google cloud 