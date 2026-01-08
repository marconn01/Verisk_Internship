# Use lightweight Nginx image to serve static files
FROM nginx:alpine

# Remove default nginx HTML files
RUN rm -rf /usr/share/nginx/html/*

# Copy ALL frontend files (HTML/CSS/JS) into nginx html folder
COPY . /usr/share/nginx/html

# Expose container port 80
EXPOSE 80
