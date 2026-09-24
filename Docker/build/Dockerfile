FROM python:3.11-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Hier installierst du deine Pakete direkt:
RUN pip install --no-cache-dir requests paho-mqtt

# Dateien in den Container kopieren
COPY mex.py .
COPY entrypoint.sh .

# Das Shell-Skript ausführbar machen
RUN chmod +x entrypoint.sh

# Das Shell-Skript als Startbefehl definieren
CMD ["./entrypoint.sh"]
