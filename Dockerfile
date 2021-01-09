FROM python:3

ENV PTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r kuvar/requirements.txt
