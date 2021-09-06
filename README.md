
# Grafana Playground


- `./bin/populate-logs.sh` - Run to write log entries to `logs/for-promtail.log` once per second.  This is ingested by Promtail.
- `./bin/run-local-promtail.sh` - Run locally on a Mac to ingest logs into Loki.  This is necessary because you cannot import `/var/log/` into Docker for OS/X.
- `./bin/query.sh` - Query the Dockerized instance of Loki on the command line.
  - Examples:
    - `./bin/query.sh '{job="varlogs"}'`
    - `./bin/query.sh '{job="varlogs"}' 5`
    - `./bin/query.sh '{job="varlogs",host="docker"}'`
    - `./bin/query.sh '{job="varlogs",filename="/var/log/system.log"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"} 10'`


## Viewing Logs

- To acccess the Grafana instance, go to [http://localhost:3000/](http://localhost:3000/)
  - Log in with username of `admin` and the password of `admin`.  Change the password if you wish.
- Hover over the `Gear` icon on the left, click `Data sources`
  - Click `Add data source`.
  - Choose `Loki` from the list.
  - For the URL, enter `http://loki:3100/`
  - Click `Save and Test`
- Hover over the plus sign (`+`) on the left, click `Import`.
  - Click `Upload JSON file` and navgiate to the file `config/log-volume-dashboard.json`, then click `Import`.
- The dashboard should now show a breakdown of all log volumes.
- To run a specific query, click the `Compass` on the left which pouts you into `Explorer Mode`.
  - Then paste in this query: `{filename="/logs/synthetic/synthetic.log}`.
  - That should immediately show you the most recent logs that have been written. If this shows nothing, then data is not making it into Loki.


## Manually Injecting Logs

If you want to manually inject an arbitrary number of logs, that can be done with this command:

- `docker-compose run logs n`

Replace `n` with the number of logs you want to write.  They will go into the file `/logs/synthetic/manual.log`
in the `logs` volume, which will then be picked up by the `promtail` container.  They can be viewed
in Grafana with this query:

- `{filename=~"/logs/synthetic/manual.log"}`


## Sending Docker Logs to Loki

Docker normally writes standard output from its containers to a file.  However, standard output
can also be sent somewhere else... such as Loki.  Even the output from Loki can be sent back to itself!
Here's how to do that:

- First, install the Docker plugin to talk to Loki:
  - `docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions`
- Now, set up a symlink so a `docker-compose.override.yml` file will be read in:
  - `ln -s docker-compose.override.yml.sample docker-compose.override.yml`
- If you are currently running any containers, you must kill and restart them as follows:
  - `docker-compose kill logs; docker-compose up -d logs`
- You can verify the container is sending its logs to Loki with a command similar to:
  - `docker inspect grafana-playground_logs_1 | jq .[].HostConfig.LogConfig`
- From there, you can view logs from all your containers in Grafana with this query:
  - `{host="docker-desktop"}`
- To import the dashboard for viewing Docker logs:
  - Hover over the plus sign (`+`) on the left, click `Import`.
    - Click `Upload JSON file` and navgiate to the file `config/log-volume-dashboard.json`, then click `Import`.
  - The dashboard should now show a breakdown of all log volumes.

More about how to configure the Docker Loki plugin [can be read here](https://grafana.com/docs/loki/latest/clients/docker-driver/configuration/).


## Development

- Working on the `logs` container
  - `docker-compose kill logs; docker-compose rm -f logs; docker-compose build logs && docker-compose up logs`
- Working on the `promtail` container
  - `docker-compose kill promtail; docker-compose rm -f promtail; docker-compose build promtail && docker-compose up promtail`



