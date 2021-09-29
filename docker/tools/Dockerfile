
FROM python:3

COPY requirements.txt /
RUN pip3 install -r /requirements.txt


COPY bootstrap.sh /
COPY entrypoint.sh /


ENTRYPOINT [ "/entrypoint.sh" ]

