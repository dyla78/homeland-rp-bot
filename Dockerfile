# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone un puerto opcional si usas Flask (para keep_alive)
EXPOSE 8080

# Comando para ejecutar tu bot
CMD ["python", "main.py"]
