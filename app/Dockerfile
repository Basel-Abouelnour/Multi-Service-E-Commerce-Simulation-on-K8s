# this is a python app that checks a connection on a specific port
# it takes two environment variables TARGET_HOST,TARGET_PORT
FROM python:alpine3.21

WORKDIR /app

RUN pip install flask

COPY ./app.py ./app.py

EXPOSE 5000

CMD ["python3", "app.py"]

