FROM osgeo/gdal:ubuntu-full-3.3.1

RUN \
  apt -y update --fix-missing && \
  apt -y install software-properties-common && \
  apt -y update && \
  apt -y upgrade && \
  apt -y install python3-pip && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt


