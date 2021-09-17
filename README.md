
# Grafana Playground

This is a little project I put together that lets you spin up a Grafana-based environment in Docker and automatically feed in logs.  That environment includes:

- Grafana, for graphing
- Loki, for storing time series logs
- A Docker container called `logs`, which automatically generates synthetic log entries.
- Promtail, for reading in the generated logs, as well as the contents of `/var/log/`.
- `ping`, a container which pings multiple hosts, using the excellent [https://cr.yp.to/daemontools.html](Daemontools package) to handle multiple instances of ping running at once.


## Getting Started

Run `docker-compose up` and this will spin up each of the containers mentioned above, making the following endpoints available:

- http://localhost:3000/ - Local Grafana instance. Login and pass are `admin/admin`.
- http://localhost:3100/ - Local Loki instance.  Check http://localhost:3100/ready to see if the instance is ready.
- http://localhost:9081/targets - Targets page for the (Dockerized) instance of promtail.


## Viewing Logs

- To acccess the Grafana instance, go to [http://localhost:3000/](http://localhost:3000/)
  - Log in with username of `admin` and the password of `admin`.  Change the password if you wish.
- Hover over the `Gear` icon on the left, click `Data sources`
  - Click `Add data source`.
  - Choose `Loki` from the list.
  - For the URL, enter `http://loki:3100/`
  - Click `Save and Test`
- Hover over the plus sign (`+`) on the left, click `Import`.
  - Click `Upload JSON file`
    - Navgiate to the file `config/dashboards/log-volume-dashboard.json`, then click `Import`.
    - Repeat with `config/log-volume-dashboard-docker-containers.json`
    - Repeat with `config/dashboards/ping-times.json`
- You now have the following dashboards available:
  - [Ping times](http://localhost:3000/d/WiThvuS7z/ping-times?orgId=1&refresh=5s)
  - [Volume by Logfile](http://localhost:3000/d/fponVrV7z/log-volume?orgId=1) - Covers syslog, synthetic logs, and ping times.
  - [Volume by Docker container](http://localhost:3000/d/RQVYi6V7k/log-volume-docker-containers?orgId=1) - This playground ingests logs from its own Docker containers, which can be viewed here.
- To run a specific query, click the `Compass` on the left which pouts you into `Explorer Mode`.
  - Then paste in this query: `{ filename=~"/logs/synthetic/.*" }`.
  - That should immediately show you the most recent logs that have been written. If this shows nothing, then data is not making it into Loki.


## Manually Injecting Logs

If you want to manually inject an arbitrary number of logs, that can be done with this command:

- `docker-compose run logs n`

Replace `n` with the number of logs you want to write.  They will go into the file `/logs/synthetic/manual.log`
in the `logs` volume, which will then be picked up by the `promtail` container.  They can be viewed
in Grafana with this query:

- `{filename=~"/logs/synthetic/manual.log"}`


## Changing Which Hosts are Pinged

- Edit `docker-compose.yml`
- Change the `HOSTS` variable for the `ping` container.
- Restart the `ping` container with `docker-compose restart ping`.


## Considerations for Mac Users

For whatever reason, I have not had any luck mapping `/var/log/` on my Mac to a Docker container.  
I tried a bunch of different things, but no luck.  I ended up coming up with a workaround, which
is to install and run Promtail locally:

- `brew install promtail`
- `./bin/run-local-promtail.sh` - Run this locally to send logs to the Dockerized version of Loki.


## Command Line Utilities

If you want to query Loki directly, I write a command-line script for that:

- `./bin/query.sh` - Query the Dockerized instance of Loki on the command line.
  - Examples:
    - `./bin/query.sh '{job="varlogs"}'`
    - `./bin/query.sh '{job="varlogs"}' 5`
    - `./bin/query.sh '{job="varlogs",host="docker"}'`
    - `./bin/query.sh '{job="varlogs",filename="/var/log/system.log"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"} 10'`


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


## Additional Considerations

- For Loki, I set `min_ready_duration` to be 5 seconds so that the database is ready quicker.
  - I would not recommend this setting for production use.
- There are some label extractions in `config/promtail-config-docker.yaml` which are commented out.
  - Feel free to uncomment them if you want to expirment with labels, but be advised the number of streams is the *product* of how many different label values you can have, which can cause performance issues.  That is explained more [in this post](https://grafana.com/blog/2020/08/27/the-concise-guide-to-labels-in-loki/)
  - TL;DR If you go crazy with labels and try to Index a high-cardinality field, you're gonna have a bad time!


## Development

- Working on the `logs` container
  - `docker-compose kill logs; docker-compose rm -f logs; docker-compose build logs && docker-compose up logs`
- Working on the `promtail` container
  - `docker-compose kill promtail; docker-compose rm -f promtail; docker-compose build promtail && docker-compose up promtail`



