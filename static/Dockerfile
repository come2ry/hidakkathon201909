FROM nginx:alpine
RUN rm -f /etc/nginx/conf.d/default.conf
COPY .config/proxy.conf /etc/nginx/conf.d
COPY . /usr/share/nginx/html
