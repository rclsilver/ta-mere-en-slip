FROM python:3.8.2-alpine3.11

CMD ["./docker-entrypoint.sh"]
EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD requirements/* /code/requirements/
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir  -r requirements/production.txt

COPY . /code
