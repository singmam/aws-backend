FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install "pymongo[srv]" uvicorn

EXPOSE 8000