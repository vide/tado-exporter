FROM python:3.7-alpine

WORKDIR /usr/src/app

EXPOSE $TADO_EXPORTER_PORT
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN apk add --no-cache git
RUN pip install --no-cache-dir -r requirements.txt

COPY init.py ./
CMD [ "python", "./init.py" ]
