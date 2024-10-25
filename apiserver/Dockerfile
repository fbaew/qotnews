FROM python:3.8-slim-buster

RUN apt-get update && apt-get install curl git gnupg2 python3-pip virtualenv yarn -y

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

WORKDIR /app

COPY . .
