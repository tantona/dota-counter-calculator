FROM python:3.7.0b3-alpine3.7

RUN apk update && apk add bash

COPY ./ /opt/dota-picker

WORKDIR /opt/dota-picker

CMD ["python", "main.py"]
