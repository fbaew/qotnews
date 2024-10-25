FROM python:3.8-slim-buster

# Install necessary packages and Yarn
RUN apt-get update && \
    apt-get install -y curl git gnupg2 python3-pip virtualenv && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -y yarn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 
    # && \
    # yarn install && \
    # yarn build

WORKDIR /app

COPY . .

RUN yarn install && \
    yarn build
