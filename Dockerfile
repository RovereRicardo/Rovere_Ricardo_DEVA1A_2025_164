# Stage 1: Base - Installation des dépendances système
FROM python:3.12-slim AS base
WORKDIR /app

# Installation des dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies - Installation des packages Python
FROM base AS dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Development - Environnement de développement
FROM dependencies AS development
COPY . .

# Configuration pour l'environnement de développement
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV VERBOSE=ON
ENV AUTO_LOGIN=admin

EXPOSE 5000

# Démarrage avec le serveur de développement Flask
CMD ["flask", "--app", "flaskr", "--debug", "run", "--host=0.0.0.0"]

# Stage 4: Production - Environnement de production
FROM dependencies AS production
COPY . .

# Configuration pour l'environnement de production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV VERBOSE=OFF
ENV AUTO_LOGIN=""

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# Démarrage avec Gunicorn en production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "flaskr:create_app()"]
