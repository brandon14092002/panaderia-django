# Imagen base con Python 3.10
FROM python:3.10.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Comando para arrancar Django con gunicorn (Render pasa $PORT)
CMD gunicorn panaderia.wsgi:application --bind 0.0.0.0:$PORT