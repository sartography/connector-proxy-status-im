FROM ghcr.io/sartography/python:3.11

RUN pip install poetry
RUN useradd _gunicorn --no-create-home --user-group

# libpq-dev for pg_config executable, which is needed for psycopg2
RUN set -xe \
  && apt-get update -q \
  && apt-get install -y -q \
        libpq-dev

# remove packages that are not needed in production.
# just for security. won't help image size.
RUN set -xe \
  && apt-get remove -y \
  gcc \
  libssl-dev \
  postgresql-client \
  python3-dev \
  && apt-get autoremove -y \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD pyproject.toml poetry.lock /app/
ADD connectors /app/connectors
RUN poetry install

COPY . /app/

# run poetry install again AFTER copying the app into the image
# otherwise it does not know what the main app module is
RUN poetry install

CMD ./bin/boot_server_in_docker
