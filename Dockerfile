FROM python:3.9.7-buster

WORKDIR /app

ADD . /app
ADD https://raw.githubusercontent.com/meow55555/stl/main/dist/stl-linux-amd64 /usr/local/bin/stl
RUN chmod a+x /usr/local/bin/stl

ENV FLASK_APP=manage
ENV FLASK_ENV=production
ENV DATABASE_URI="sqlite:///data.db"

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD flask run --host 0.0.0.0 --port 8080
