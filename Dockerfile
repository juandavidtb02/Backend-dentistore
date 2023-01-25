FROM python:3.10.4-alpine3.15


ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk add musl-dev mariadb-dev gcc
RUN pip install mysqlclient

WORKDIR /app


COPY ./requeriments.txt ./

RUN pip install -r requeriments.txt

COPY ./ ./

EXPOSE 8000
CMD ["sh","entrypoint.sh"]
