FROM python:3.9.1-alpine3.12
RUN mkdir /app
COPY ["flask_jwt_authenticator/*", "requirements.txt", "/app/"]
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "__init__.py" ]