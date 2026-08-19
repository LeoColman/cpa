FROM nginx:1.27-alpine
COPY index.html      /usr/share/nginx/html/index.html
COPY identidade.html /usr/share/nginx/html/identidade.html
COPY formulario.html /usr/share/nginx/html/formulario/index.html
COPY estatuto.html   /usr/share/nginx/html/estatuto/index.html
COPY estatuto-cpa-2026.pdf /usr/share/nginx/html/estatuto-cpa-2026.pdf
COPY favicon.svg     /usr/share/nginx/html/favicon.svg
COPY shared/         /usr/share/nginx/html/shared/
EXPOSE 80
