# syntax=docker/dockerfile:1.5-labs
FROM datasetteproject/datasette:0.64.1
LABEL maintainer="hello@vizzuality.com"

ENV NAME custom-datasette
ENV USER $NAME
ENV APP_HOME /opt/$NAME

ARG DATASETTE_SQLITE_DB_FILENAME
ARG DATA_CORE_SQLITE_DB_SOURCE_URL
ARG DATASETTE_CORS_ORIGINS

RUN addgroup $USER && useradd --shell /bin/bash --gid $USER $USER

WORKDIR $APP_HOME
RUN chown $USER:$USER $APP_HOME

# install Datasette plugins and any other libraries needed
RUN pip install datasette-cors

# # populate data folder
# COPY --chown=$USER:$USER data ./data
# ADD --chown=$USER:$USER --checksum=${DATA_CORE_SQLITE_DB_CHECKSUM} ${DATA_CORE_SQLITE_DB_SOURCE_URL} ./data/${DATASETTE_SQLITE_DB_FILENAME}
# RUN find ./data -type f -exec chmod ugo-w '{}' \;

# handle Datasette configuration via metadata.json
# COPY metadata.json.template ./
# COPY scripts ./scripts
ENV DATASETTE_CORS_ORIGINS $DATASETTE_CORS_ORIGINS
RUN scripts/set-cors-origins-in-metadata.sh > metadata.json
RUN chmod ugo-w metadata.json
RUN rm metadata.json.template

EXPOSE 3000
USER $USER

# @todo Consider whether to use a shell script as entrypoint to allow for
# different run modes (e.g. debug, dev, prod, etc.) via Docker commands
CMD datasette --metadata metadata.json --host 0.0.0.0 --port 3000 --setting base_url /data/ data/${DATASETTE_SQLITE_DB_FILENAME}
