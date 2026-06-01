FROM nginx:latest

RUN rm -rf /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# Remove sym links from nginx image
RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log

# Install logrotate
RUN apt-get update && apt-get -y install logrotate

# Create old_logs dir 
RUN mkdir -p /var/log/nginx/old_logs

COPY --chown=root:root ./entrypoint.sh /
# Copy logrotate
COPY --chown=root:root ./logrotate /etc/logrotate.d/nginx

RUN chmod 644 /etc/logrotate.d/nginx

ENTRYPOINT ["/entrypoint.sh"]