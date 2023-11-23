FROM python:3.12-alpine

WORKDIR /app
COPY /source/entrypoint.sh entrypoint.sh
COPY /source/requirements.txt requirements.txt
COPY /source/calico-ipset.py calico-ipset.py

RUN apk update && apk add yq bash curl
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
