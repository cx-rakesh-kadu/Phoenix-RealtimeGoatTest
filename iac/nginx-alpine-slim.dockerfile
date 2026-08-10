FROM nginx:1.29.1-alpine3.22-slim
RUN mkdir -p /var/cache/nginx/client_temp \
    && chown -R nginx:nginx /var/cache/nginx \
    && mkdir -p /run/nginx \
    && chown -R nginx:nginx /run/nginx

# Use nginx user for Alpine-based nginx image compatibility# Expose default HTTP port
EXPOSE 80

# Start nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
