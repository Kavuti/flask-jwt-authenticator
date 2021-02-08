FROM python:3.9.1-alpine3.12 as python-alpine
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

FROM python-alpine
RUN mkdir /app
COPY ["/", "init.sql", "requirements.txt", "/app/"]
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/flask_jwt_authenticator
ENV FLASK_APP=app.py

ENTRYPOINT [ "gunicorn", "-w 4", "--bind=0.0.0.0", "app:app" ]