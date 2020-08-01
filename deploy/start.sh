#!/bin/bash

docker stop pca
docker rm -f pca
docker run -itd --name pca -p 9010:5001 -v $PWD/pca:/app -w /app --entrypoint "./manager" -e LC_ALL=zh_CN.utf8 -e LANG=zh_CN.utf8 -e LANGUAGE=zh_CN.utf8  pca_base:1.0 /bin/bash
docker cp /usr/share/zoneinfo/ pca:/usr/share
docker exec -it pca /bin/bash -c 'cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime'