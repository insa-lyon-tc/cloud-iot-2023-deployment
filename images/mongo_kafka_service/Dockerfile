# Utiliser l'image de base Python
FROM python:3.8

# Créer et définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requis dans le conteneur
COPY script.py /app/
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Enable kubernetes logging
ENV PYTHONUNBUFFERED=1

# Commande pour exécuter le script Python
CMD ["python3", "script.py"]
