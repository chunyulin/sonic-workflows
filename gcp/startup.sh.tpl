#!/bin/bash
/opt/deeplearning/install-driver.sh
mkdir ${FOLDER}/models
gcsfuse --implicit-dirs tw-nchc ${FOLDER}/models
docker run -d --gpus=1 --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 \
       --mount type=bind,source=${FOLDER}/models/models,target=/srv \
       nvcr.io/nvidia/tritonserver:21.02-py3 \
       tritonserver --model-repository=/srv/${mo}
