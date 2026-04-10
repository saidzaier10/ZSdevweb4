# Stage 1: Build Vue frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

# Stage 2: Nginx avec les assets Vue
FROM nginx:1.25-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/nginx.prod.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-builder /app/dist /usr/share/nginx/html

RUN mkdir -p /var/www/static /var/www/media

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
