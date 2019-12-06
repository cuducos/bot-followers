FROM python:3.8.0-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONBREAKPOINT=ipdb.set_trace

WORKDIR /web

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
COPY manage.py manage.py

RUN set -ex && \
    apt-get update && \
    apt-get install -y gcc libpq-dev && \
    python -m pip --no-cache install -U pip pipenv && \
    pipenv install --dev --system && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]