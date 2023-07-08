FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/SiteForOlympic

COPY ./req.txt /usr/src/req.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/req.txt

COPY . /usr/src/SiteForOlympic


