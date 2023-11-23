FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txtb

COPY . /app/
