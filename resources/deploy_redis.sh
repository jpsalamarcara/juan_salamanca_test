#!/usr/bin/env bash
docker pull redis:5.0.7

docker network create mycompany.com

docker run --name region1 --network mycompany.com  -p 6379:6379 -d redis:5.0.7

docker run -it --network mycompany.com --rm redis redis-cli -h region1