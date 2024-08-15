# Dockerfile for Vite Frontend
FROM node:20.16.0-alpine3.20

WORKDIR /app

# Удаление node_modules и package-lock.json перед установкой зависимостей
RUN rm -rf node_modules package-lock.json

COPY package*.json ./

RUN npm install --legacy-peer-deps

COPY . .

CMD ["npm", "run", "dev"]