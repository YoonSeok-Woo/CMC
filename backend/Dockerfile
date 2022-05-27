FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["gunicorn", "--certfile=/etc/letsencrypt/live/j6a502.p.ssafy.io/fullchain.pem", "--keyfile=/etc/letsencrypt/live/j6a502.p.ssafy.io/privkey.pem", "cmc.wsgi:application", "--bind", "0.0.0.0:8000"]