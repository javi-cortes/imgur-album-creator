FROM python:3.9.5

RUN apt update

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONBUFFERED=1
COPY . /imgur_crawler

WORKDIR /imgur_crawler/imgur_crawler

CMD ["scrapy", "crawl", "imgur_crawler"]