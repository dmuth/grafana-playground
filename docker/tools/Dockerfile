
FROM python:3

COPY requirements.txt /
COPY entrypoint.sh /

RUN pip3 install -r /requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]

