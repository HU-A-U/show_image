FROM ubuntu:16.04
MAINTAINER hu_a_u@163.com
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code
COPY show.py show.py
RUN python show.py runserver

EXPOSE 6666