# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/tasks

# Set work directory
WORKDIR /tasks

# Install dependencies
COPY ./poetry.lock ./pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false --local &&  poetry install

# Copy project
COPY . .

EXPOSE 8001

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8001

