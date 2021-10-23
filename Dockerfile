FROM python:3.9.7-buster

WORKDIR /app

ADD . /app

ENV FLASK_APP=manage
ENV FLASK_ENV=production
ENV DATABASE_URI="sqlite:///data.db"

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD flask run --host 0.0.0.0 --port 8080
