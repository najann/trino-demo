# Stock Price Prediction to demonstrate Trino capabilities

This demo is intended to show the central Trino features by accessing data from PostgreSQL, MongoDB and Kafka.
It is not meant to produce serious stock price predictions (general disclaimer)!

## Running on Kubeflow

Assuming you have Kubeflow running on an Openshift (on ppc64le) or vanilla k8s cluster, you can use the respective instructions in [`openshift_trino_demo_installation.txt`](./openshift_trino_demo_installation.txt) and [`vanilla_k8s_trino_demo_installation.txt`](vanilla_k8s_trino_demo_installation.txt) to setup the databases and trino server needed for the demo.
Then, [`KubeflowStockPricePrediction.ipynb`](KubeflowStockPricePrediction.ipynb) defines a component, to connect to and query Trino.
This is used multiple times throught the demo pipeline.

## Running locally

To run the demo locally, you can use [the setup script](./local_demo_setup/setup.sh).
It assumes you set the following aliases according to your environment:
- `startpostgre`: starts a local PostgreSQL server on port 5432. To be able to properly connect to your database, consult [`trino_postgresql_local_connect.md`](./local_demo_setup/trino_postgresql_local_connect.md).
- `activatenv`: creates and/or activates a Python environment.

Moreover, you need to update the catalog definitions in [`trino/catalog/*.properties`](./trino/catalog) beforehand.
Then, the setup script will start your PostgreSQL server, a MongoDB container, a Kafka cluster (defined in [`docker-compose.yaml`](./local_demo_setup/docker-compose.yaml)) and the Trino server.

Use [`fillMongoDB.ibpynb`](./local_demo_setup/fillMongoDB.ibpynb), [`fill_postgresql.sql`](./local_demo_setup/fill_postgresql.sql) and the Python producer scripts (for stock prices & weather) to fill all databases with the needed data.
In some of the Python scripts, you will be prompted to provide your API-key for RapidAPI and stockdata.org.
Once the data is loaded, you should be able to run [`localTrinoTest.ipnyb`](./local_demo_setup/localTrinoTest.ipnyb).

The setup can be stopped with [`teardown.sh`](./local_demo_setup/teardown.sh).