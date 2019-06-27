FROM python:3

MAINTAINER "Lance Finn Helsten" <lanhel@flyingtitans.com>

WORKDIR ${CF_VOLUME_PATH:-/usr/src}/ZeffClient

COPY . ${CF_VOLUME_PATH:-/usr/src}/ZeffClient

RUN make install

CMD [ "bash" ]

