FROM nginx:1.25-alpine

# Supprimer la config nginx par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copier notre configuration de production
COPY nginx.prod.conf /etc/nginx/conf.d/default.conf

# Créer les répertoires pour les fichiers statiques
RUN mkdir -p /var/www/static /var/www/media

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
