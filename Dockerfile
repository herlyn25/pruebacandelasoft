FROM python:3.10-alpine

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip

COPY .env /app/.env
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python","manage.py","runserver","0.0.0.0:8000"]