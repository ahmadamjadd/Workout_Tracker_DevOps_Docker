# Stage 1: Build the React app
FROM node:22 AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# Stage 2: Serve with Ubuntu-based Apache
FROM ubuntu/apache2:latest

# Remove the default index page
RUN rm -rf /var/www/html/*

# Copy the built files from the 'build' stage
# In ubuntu/apache2, the default web root is /var/www/html/
COPY --from=build /app/dist/ /var/www/html/

EXPOSE 80

