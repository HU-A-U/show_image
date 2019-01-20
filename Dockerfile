FROM ubuntu:16.04
MAINTAINER hu_a_u@163.com

RUN sudo apt-get install python:3.6
RUN sudo apt-get install python-pip


ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /code
WORKDIR /code
COPY . /code

COPY show.py show.py
RUN chmod +x show.sh

CMD /code/show.sh

EXPOSE 6666