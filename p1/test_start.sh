#!/usr/bin/env bash

cp env.example app/.env
docker pull postgres
docker network create test_network
docker run --network=test_network -d --name test -p 5432:5432 \
       -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
       -e POSTGRES_DB=postgres postgres -N 2000
docker build . -t test_python
docker run --network=test_network --name test_p test_python /bin/bash -c "python -m pytest -v ."
docker container stop test test_p
docker container rm test test_p
docker network rm test_network

