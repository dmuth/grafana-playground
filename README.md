
# Grafana Playground


- `./bin/populate-logs.sh` - Run to write log entries to `/var/log/for-promtail.log` and `logs/for-dockerized-promtail.log` once per second.
- `./bin/run-local-promtail.sh` - Run locally on a Mac to ingest logs into Loki.  This is necessary because you cannot import `/var/log/` into Docker for OS/X.
- `./bin/query.sh` - Query the Dockerized instance of Loki.


