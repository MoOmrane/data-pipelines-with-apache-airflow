# Data Pipelines with Apache Airflow

This repository builds upon the original code examples by adding modern implementations adapted for **Apache Airflow 3**. It serves as a bridge between the concepts presented in the book and the latest Airflow practices.

### Structure

Overall, this repository is structured as follows:

```
├── chapter01                # Original code examples for Chapter 1.
├── chapter01_airflow3       # Airflow 3 implementation for Chapter 1.
├── chapter02                # Original code examples for Chapter 2.
├── chapter02_airflow3       # Airflow 3 implementation for Chapter 2.
├── ...
```

Code for each Chapter is generally structured something like follows:

```
├── dags                  # Airflow DAG examples (+ other code).
├── docker-compose.yml    # Docker-compose file used for running the Chapter's containers.
└── readme.md             # Readme with Chapter-specific details, if any.
```

### Usage

Details for running specific chapter examples are available in the corresponding chapter's readme.