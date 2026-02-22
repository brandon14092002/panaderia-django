# Imagen base con Python 3.10
FROM python:3.10.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto que Render usa
EXPOSE 8000

# Comando para arrancar Django con gunicorn
CMD gunicorn panaderia.wsgi:application --bind 0.0.0.0:$PORT