# The calculator is one self-contained page, so the server is just nginx
# serving static files on :8080 behind Fly.io's proxy (which does TLS).
FROM nginx:stable-alpine

# our server block replaces nginx's default site
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

# the page keeps its readable name in the repo; on the web it is the site root
COPY ["Artillery & Mortar Calculator.html", "/usr/share/nginx/html/index.html"]
COPY privacy.html /usr/share/nginx/html/privacy.html

# the logo and tab icons (deploy/make-icons.py builds them)
COPY img/ /usr/share/nginx/html/img/

# robots.txt, and ads.txt once AdSense is set up (see DEPLOY.md)
COPY site/ /usr/share/nginx/html/

EXPOSE 8080
