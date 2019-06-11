FROM python:3.7.3-slim-stretch


RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get clean all

RUN mkdir -p /restock/build
COPY ./ /restock/build/

RUN cd /restock/build \
    && python3 setup.py sdist \
    && cd dist \
    && pip install -U $(ls)  \
    && rm -r /restock/build


CMD ["gunicorn", "-b", "0.0.0.0:10000", "restock.restock:app"]
