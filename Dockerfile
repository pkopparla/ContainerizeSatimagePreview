# FROM osgeo/gdal:ubuntu-full-3.3.1
FROM osgeo/gdal:alpine-normal-latest

# RUN \
#   apt -y update --fix-missing && \
#   apt -y install software-properties-common && \
#   apt -y update && \
#   apt -y upgrade && \
#   apt -y install python3-pip && \
#   rm -rf /var/lib/apt/lists/*
RUN apk add --update py-pip

WORKDIR /workspace
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
