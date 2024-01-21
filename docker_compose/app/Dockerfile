FROM python:3.8.10-slim
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN python manage.py migrate
COPY . .
EXPOSE 8000
# CMD gunicorn -b 0.0.0.0:8000 stocks_products.wsgi