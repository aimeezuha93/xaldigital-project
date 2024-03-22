FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV APP_HOME /usr/src/app

WORKDIR /$APP_HOME

RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . $APP_HOME/

EXPOSE 3001

CMD [ "flask", "run", "--host=0.0.0.0", "--port=3001"]