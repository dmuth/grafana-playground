
# Grafana Playground


- `./bin/populate-logs.sh` - Run to write log entries to `logs/for-promtail.log` once per second.  This is ingested by Promtail.
- `./bin/run-local-promtail.sh` - Run locally on a Mac to ingest logs into Loki.  This is necessary because you cannot import `/var/log/` into Docker for OS/X.
- `./bin/query.sh` - Query the Dockerized instance of Loki.
  - Examples:
    - `./bin/query.sh '{job="varlogs"}'`
    - `./bin/query.sh '{job="varlogs"}' 5`
    - `./bin/query.sh '{job="varlogs",host="docker"}'`
    - `./bin/query.sh '{job="varlogs",filename="/var/log/system.log"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"}'`
    - `./bin/query.sh '{job="varlogs",filename=~"/var.*"} 10'`



## Development

- Working on the `logs` container
  - `docker-compose kill logs; docker-compose rm -f logs; docker-compose build logs && docker-compose up -d logs && docker-compose logs -f logs`



