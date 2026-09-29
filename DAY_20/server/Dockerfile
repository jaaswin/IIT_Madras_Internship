FROM php:8.2-apache

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        perl \
        make \
        gcc \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd \
    && rm -rf /var/lib/apt/lists/*

# Install patched ExifTool 13.59
COPY Image-ExifTool-13.59.tar.gz /tmp/Image-ExifTool-13.59.tar.gz

RUN mkdir -p /tmp/exiftool \
    && tar -xzf /tmp/Image-ExifTool-13.59.tar.gz \
        -C /tmp/exiftool \
    && cd /tmp/exiftool/Image-ExifTool-13.59 \
    && perl Makefile.PL \
    && make install \
    && cd / \
    && rm -rf /tmp/exiftool \
    && rm -f /tmp/Image-ExifTool-13.59.tar.gz

RUN mkdir -p /var/www/html/uploads \
    && mkdir -p /var/www/html/previews \
    && chown -R www-data:www-data /var/www/html/uploads \
    && chown -R www-data:www-data /var/www/html/previews \
    && chmod 755 /var/www/html/uploads \
    && chmod 755 /var/www/html/previews

COPY index.php /var/www/html/index.php
COPY login.php /var/www/html/login.php
COPY dashboard.php /var/www/html/dashboard.php
COPY upload.php /var/www/html/upload.php
COPY status.php /var/www/html/status.php

EXPOSE 80
COPY api /var/www/html/api
