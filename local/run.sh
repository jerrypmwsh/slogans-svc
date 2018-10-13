#!/usr/bin/env bash
set -xe

pushd ..
./build.sh
popd

docker-compose up
