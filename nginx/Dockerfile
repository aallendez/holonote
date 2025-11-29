FROM nginx:alpine

# Install AWS CLI
RUN apk add --no-cache aws-cli

# Copy nginx configuration
COPY nginx/nginx.prod.conf /etc/nginx/conf.d/default.conf

# Copy entrypoint script
COPY nginx/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directory for static files
RUN mkdir -p /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
