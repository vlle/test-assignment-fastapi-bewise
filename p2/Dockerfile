FROM python:3.11

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get -y update && apt-get -y upgrade &&\
    apt-get install ffmpeg -y &&\
    pip install --no-cache-dir --upgrade  -r requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]

