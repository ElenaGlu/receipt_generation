FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN apt-get update && apt-get install -y wkhtmltopdf

RUN python -m pip install --upgrade pip
RUN pip install --upgrade poetry && poetry --version

RUN poetry install

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



