FROM php:cli

RUN apt-get update && apt-get install -y git zip unzip
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
WORKDIR /usr/src/app
COPY composer.json composer.lock ./
RUN composer install

COPY . .

