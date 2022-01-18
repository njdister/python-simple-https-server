#!/usr/bin/env bash

get_parameter() {
    aws --output text --query Parameter.Value ssm get-parameter --name $1 --with-decryption 
}

export SERVER_PORT="$(get_parameter '/bb2/test/python-simple-https-server/server-port')"
export SERVER_KEY="$(get_parameter '/bb2/test/python-simple-https-server/server-key')"
export SERVER_CERT="$(get_parameter '/bb2/test/python-simple-https-server/server-cert')"

docker run --rm \
    -e SERVER_PORT \
    -e SERVER_KEY \
    -e SERVER_CERT \
    -p $SERVER_PORT:$SERVER_PORT \
    python-simple-https-server:latest