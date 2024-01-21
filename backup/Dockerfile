FROM postgres:13

COPY backup.sh /backup.sh

RUN mkdir /backups

RUN chmod +x /backup.sh

CMD while true; do /backup.sh; sleep 10800; done
