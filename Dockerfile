# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /dslinter
COPY . .
RUN pip install -e .
RUN pip install pytest

# RUN pytest