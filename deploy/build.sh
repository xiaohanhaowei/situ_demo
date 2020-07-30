#!/bin/bash

docker run -itd --name temp pca_base:v1 /bin/bash
docker cp pca temp:/pca
docker commit temp pca_base:1.0
docker rm -f temp