FROM python:3.10

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

WORKDIR /app

COPY pyproject.toml .

RUN pip install --upgrade pip

RUN pip3 install poetry==1.3.2
RUN poetry config virtualenvs.create false
RUN --mount=type=ssh poetry install

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]
