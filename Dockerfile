FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --upgrade setuptools   \
    && python3 -m pip install "pymongo[srv]" uvicorn fastapi passlib crypto pycrypto python-jose[cryptography] python-multipart python-dotenv python-jose
    

COPY ./* /home/app

EXPOSE 8000

CMD ["python3", "/home/app/main.py"]