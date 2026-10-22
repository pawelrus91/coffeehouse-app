FROM python:3.13

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=2.5.1 \
    POETRY_VIRTUALENVS_CREATE=0

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . /app/

RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]