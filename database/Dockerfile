FROM mysql:5.7

# environment variables
ENV http_proxy http://10.239.4.80:913
ENV https_proxy http://10.239.4.80:913

VOLUME /var/lib/mysql

COPY docker-entrypoint.sh /usr/local/bin/
COPY mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 3306 33060
CMD ["mysqld"]
