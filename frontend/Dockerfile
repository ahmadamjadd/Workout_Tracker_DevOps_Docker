FROM node:22 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM ubuntu/apache2:latest

RUN rm -rf /var/www/html/*

COPY --from=build /app/dist/ /var/www/html/

EXPOSE 80

