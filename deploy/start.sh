#!/bin/bash

docker stop pca
docker rm -f pca
docker run -itd --name pca -p 5001:5001 -v $PWD/pca:/app -w /app --entrypoint "./manager" -e LC_ALL=zh_CN.utf8 -e LANG=zh_CN.utf8 -e LANGUAGE=zh_CN.utf8  pca_base:1.0 /bin/bash