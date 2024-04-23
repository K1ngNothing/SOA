#!/bin/bash

mkdir -p 'generated'
cp post-service.proto generated/post-service.proto
python3 -m grpc_tools.protoc -I. --python_out=generated --pyi_out=generated --grpc_python_out=generated ./post-service.proto
protol -o generated --in-place protoc -p . post-service.proto  # fix imports in generated code