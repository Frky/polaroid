FROM python:3.5.2

RUN apt-get update
RUN apt-get -y install rubygems ruby-2.3
RUN gem install --no-rdoc --no-ri sass -v 3.4.22
RUN gem install --no-rdoc --no-ri compass

RUN pip install uwsgi

RUN mkdir -p /app/polaroid
COPY requirements.txt /app/polaroid
WORKDIR /app

RUN pip install -r polaroid/requirements.txt

COPY ./ /app
WORKDIR /app/website/static/polaroid
RUN compass compile

WORKDIR /app

RUN ./manage.py collectstatic --noinput -c

CMD uwsgi \
        --http :8000 \
        --module polaroid.wsgi \
        --socket polaroid.sock \
        --chmod-socket=776
