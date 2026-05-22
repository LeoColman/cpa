FROM nginx:1.27-alpine
COPY index.html      /usr/share/nginx/html/index.html
COPY identidade.html /usr/share/nginx/html/identidade.html
COPY favicon.svg     /usr/share/nginx/html/favicon.svg
COPY shared/         /usr/share/nginx/html/shared/
EXPOSE 80
