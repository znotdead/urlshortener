FROM python:latest

RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        sqlite3 \
--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y git-core

ENV DJANGO_VERSION 2.0.1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN git config --system user.name docker && git config --system user.email docker@localhost

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
