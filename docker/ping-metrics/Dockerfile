
FROM python:3

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY python-prometheus-metrics.py /
COPY python-tail-logs.py /

COPY entrypoint.sh /


ENTRYPOINT [ "/entrypoint.sh" ]

