FROM python:3.9.1-alpine3.12
RUN mkdir /app
COPY ["flask_jwt_authenticator/*", "requirements.txt", "/app/"]
ENV FLASK_APP=app.py

WORKDIR /app
RUN pip install -r requirements.txt && \
    flask db init && \
    flask db migrate && \
    flask db upgrade
CMD [ "python", "app.py" ]