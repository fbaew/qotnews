FROM python:3.8-slim-buster

RUN apt-get update && apt-get install wget -y

# RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
# RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

WORKDIR /app

COPY . .

RUN wget https://github.com/meilisearch/meilisearch/releases/download/v0.27.0/meilisearch-linux-amd64
RUN chmod +x meilisearch-linux-amd64
