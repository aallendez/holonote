# Build stage: Build the React Router app
FROM node:20-alpine AS build-env
COPY . /app/
WORKDIR /app
RUN npm ci
RUN npm run build

# Production stage: Nginx with static files
FROM nginx:alpine

# Copy static files from build to nginx html directory
COPY --from=build-env /app/build/client /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.prod.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Nginx starts automatically, no CMD needed
