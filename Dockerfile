FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apk add --no-cache git
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./init.py" ]
