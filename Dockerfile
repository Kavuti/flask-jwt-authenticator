FROM python:3.9.1-alpine3.12 as python-alpine
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

FROM python-alpine
RUN mkdir /app
COPY ["*", "/app/"]
WORKDIR /app
ENV FLASK_APP=/flask_jwt_authenticator/app.py
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "-w 4", "--bind=0.0.0.0", "app:app" ]