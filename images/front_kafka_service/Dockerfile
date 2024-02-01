# Utilisez une image de base Node.js
FROM node:14

# Définissez le répertoire de travail dans le conteneur
RUN ls
WORKDIR /app
# Copiez les fichiers package.json et package-lock.json dans le conteneur
COPY my-web-app/package*.json ./

# Installez les dépendances
RUN npm install

# Copiez le reste des fichiers de l'application dans le conteneur
COPY my-web-app/ .

# Exposez le port sur lequel l'application écoutera
EXPOSE 3000

# Commande pour démarrer l'application
CMD ["node", "app.js"]
