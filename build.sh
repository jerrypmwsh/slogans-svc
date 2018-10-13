#!/usr/bin/env bash
docker build -t slogansvc:latest .
docker build -t slogansvcnginx:latest -f Dockerfile.nginx .
