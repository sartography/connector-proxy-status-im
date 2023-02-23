FROM ghcr.io/sartography/python:3.11 AS base

ARG commit

# Prepare Python virtual environment
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN useradd _gunicorn --no-create-home --user-group

WORKDIR /app

FROM base AS setup

RUN pip install poetry
# libpq-dev for pg_config executable, which is needed for psycopg2
RUN apt-get update -q \
 && apt-get install -y -q \
        libpq-dev

ADD pyproject.toml poetry.lock /app/
ADD connectors /app/connectors
RUN poetry install

COPY . /app/

# run poetry install again AFTER copying the app into the image
# otherwise it does not know what the main app module is
RUN poetry install

FROM base AS final

LABEL source="https://github.com/sartography/connector-proxy-status-im"
LABEL description="Connector gateway for external services."

COPY --from=setup /app /app

ENTRYPOINT ["/app/bin/boot_server_in_docker"]
