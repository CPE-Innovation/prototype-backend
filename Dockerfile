# DEV ! NOT PROD

FROM python:3.11-alpine

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]
CMD ["app.py"]