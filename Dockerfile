FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

WORKDIR /app

COPY pyproject.toml .

RUN pip install --upgrade pip

RUN pip3 install poetry==1.5.0
RUN poetry config virtualenvs.create false
RUN --mount=type=ssh poetry install

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]
