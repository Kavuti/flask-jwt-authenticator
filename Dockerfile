FROM python:3.9.1-alpine3.12 as python-alpine
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev

FROM python-alpine
RUN mkdir /app
COPY ["*", "/app/"]
WORKDIR /app
ENV FLASK_APP=app.py
RUN pip install -r requirements.txt
RUN pwd && ls
RUN flask db migrate && \
    flask db upgrade
CMD [ "python", "app.py" ]