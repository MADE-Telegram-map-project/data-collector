ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-buster as builder

WORKDIR /home/app

RUN python -m venv /opt/venv

COPY ./requirements.txt ./

ENV PATH=/opt/venv/bin:${PATH}

RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip pip install -r ./requirements.txt

FROM python:${PYTHON_VERSION}-slim

ENV TZ="Europe/Moscow"

RUN apt update && \
    apt install -y --no-install-recommends libpq5 && \
    apt remove

COPY --from=builder /opt/venv /opt/venv

ENV PATH=/opt/venv/bin:${PATH}

WORKDIR /home/app

COPY ./ddl ./ddl

COPY ./config.yaml ./log_config.yaml ./

COPY ./data ./data

COPY ./db_seed ./db_seed

COPY ./main.py ./

ENV LOG_CONFIG=./log_config.yaml

CMD python ./main.py -c ./config.yaml