#!/usr/bin/env bash

cp env.example app/.env
docker-compose up --build
