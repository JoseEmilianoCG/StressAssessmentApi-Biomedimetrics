# Especificar la versión de Python
FROM python:3.12.3-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT 5000

# Establecer el directorio de trabajo
WORKDIR $APP_HOME

# Copiar los archivos del proyecto al directorio de trabajo
COPY . ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar la aplicación (using the shell form of CMD to expand $PORT)
#CMD gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 main:app
CMD ["sh", "-c", "gunicorn --bind :${PORT} --workers 1 --threads 8 --timeout 0 app.main:app"]
#CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app