shopt -s expand_aliases
source ~/.zshrc
docker-compose stop
docker rm trino_kubeflow_kafka_1
docker rm trino_kubeflow_zookeeper_1
docker stop trino && docker rm trino
docker stop mongodb && docker rm mongodb
docker network rm trino_kubeflow_app-tier app-tier
stoppostgre
