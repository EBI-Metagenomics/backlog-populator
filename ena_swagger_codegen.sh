#!/usr/bin/env bash
swagger-codegen generate -i ena_api_swagger.json -l python -o ena_swagger_client;
cp -r ena_swagger_client/swagger_client .
