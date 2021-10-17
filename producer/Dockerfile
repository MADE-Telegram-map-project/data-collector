ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}-buster

ARG TZ="Europe/Moscow"

RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

RUN apt update && \
    apt install -y --no-install-recommends libpq5 && \
    apt remove

WORKDIR /home/app

COPY ./requirements.txt ./

RUN --mount=type=cache,id=pip-cache,target=/root/.cache/pip pip install -r ./requirements.txt

COPY ./main.py ./

CMD python ./main.py