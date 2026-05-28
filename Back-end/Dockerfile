FROM python:3.9-slim

WORKDIR /app

# On installe les outils nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le code
COPY . .

# On dit à Docker que ce conteneur écoute sur le port 5001
EXPOSE 5001

# Les commandes de démarrage
CMD ["python", "app.py"]
