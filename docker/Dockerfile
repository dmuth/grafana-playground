
FROM alpine

RUN apk add bash

COPY populate-logs.sh /
COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

