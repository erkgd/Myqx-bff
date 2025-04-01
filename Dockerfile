# Imagen base oficial de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que la salida de Python se envíe directamente a la terminal sin buffering
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip

# Copia requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia el resto del código
COPY . /app/

# Recolecta archivos estáticos
RUN python manage.py collectstatic --noinput

# Ejecuta las migraciones de la base de datos
RUN python manage.py migrate

# Establece usuario no privilegiado para seguridad
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer el puerto en el que corre Django
EXPOSE 8000

# Script para iniciar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myqx_bff.wsgi:application"]