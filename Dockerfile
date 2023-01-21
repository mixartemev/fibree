FROM python:slim

# copy all files to image
COPY . ./

# install deps
RUN apt update; apt install graphviz -y; pip install poetry; poetry install --no-dev

# forwarding env vars from gitlab ci
ARG BT
ENV BT="${BT}"
ARG WH_HOST
ENV WH_HOST="${WH_HOST}"
ARG WH_PATH
ENV WH_PATH="${WH_PATH}"
ARG LOG_LEVEL='INFO'
ENV LOG_LEVEL="${LOG_LEVEL}"

# apply migrations and run bot
ENTRYPOINT poetry run alembic upgrade head; poetry run python -O -m app
