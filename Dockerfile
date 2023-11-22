FROM python:3.12-alpine

WORKDIR /app
COPY /source/entrypoint.sh entrypoint.sh
COPY /source/calico-ipset.py calico-ipset.py

RUN apk update && apk add yq bash curl

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
