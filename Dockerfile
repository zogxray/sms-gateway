FROM tiangolo/uwsgi-nginx-flask:python3.6
LABEL maintainer "Pavlov Viktor <zogxray@gmail.com>"
COPY requirements.txt ./
WORKDIR /app
RUN pip install -r ./requirements.txt --no-cache-dir
COPY . .
ENV FLASK_APP=app.py
CMD python db.py migrate --no-interaction && python db.py db:seed --no-interaction && flask run -h 0.0.0.0 -p 5000

FROM debian:latest
LABEL maintainer "Pavlov Viktor <zogxray@gmail.com>"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python db.py migrate --no-interaction
RUN python db.py db:seed --no-interaction
ENTRYPOINT ["python"]
CMD ["app.py"]
