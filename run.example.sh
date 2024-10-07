#!/bin/bash

docker stop AgrinvestAPI
docker rm AgrinvestAPI

docker build -t agrinvest-api:latest .

docker run -d -p 5001:5000 \
    -e PORT=5000 \
    -e POSTGRES_USER=seu_usuario \
    -e POSTGRES_PASSWORD=sua_senha \
    -e POSTGRES_DB=sua_base_de_dados \
    -e JWT_SECRET_KEY=sua_chave_secreta_jwt \
    -e BLOWFISH_KEY="sua_blowfish_key" \
    -e GRAYLOG_HOST=sua_graylog_host \
    -e GRAYLOG_PORT=sua_graylog_port \
    --name AgrinvestAPI agrinvest-api:latest