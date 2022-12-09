shopt -s expand_aliases
source ~/.zshrc
activatenv
docker network create app-tier
docker-compose up -d
docker run --name trino -d -p 8080:8080 -v $PWD/trino/catalog:/etc/trino/catalog --volume $PWD/trino/kafka:/etc/trino/kafka --network trino_kubeflow_app-tier --add-host=database:$(ipconfig getifaddr en0) trinodb/trino:latest
docker run -it --name mongodb -v $PWD/trino/mongo:/data/db --network trino_kubeflow_app-tier -p 27017:27017 -d mongo  
if [[ $1 == postgre ]]; then
    startpostgre
fi
jupyter