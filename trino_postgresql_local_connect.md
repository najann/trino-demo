# Connect TrinoInContainers to locally running postgresql

Create a connection properties file in `trino_data` as shown below:
```
connector.name=postgresql
connection-url=jdbc:postgresql://database:5432/<POSTGRES_DB>
connection-user=<POSTGRES_USER>
connection-password=<POSTGRES_PWD>
```
Set the environment variables `POSTGRES_USER, POSTGRES_PWD, POSTGRES_DB` according to your needs.

Then, modify `postgresql.conf` (could be found in `/usr/local/var/postgres/` [on mac]) to listen to your connections from your local IP by setting `listen_addresses = '<your_ip>'`.

Alike, add a new line at the end of `pg_hba.conf` (same folder), which looks like:
```
host	all		<your_user>		<your_ip>/0		trust'
```
Issue the following command to start a trino container:
```
docker run --name trino -d -p 8080:8080 --volume $PWD/trino_data:/etc/trino/catalog --add-host=database:$(ipconfig getifaddr en0) trinodb/trino
```
As you can see, it mounts the catalog-properties file into the container to make the postgresql connector available and sets the host "database" used in this file to your local IP so that the database accepts connection from the trino container.