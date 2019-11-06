FROM mysql:5.7

# environment variables
ENV http_proxy http://10.239.4.80:913
ENV https_proxy http://10.239.4.80:913
ENV GOSU_VERSION 1.7
ENV MYSQL_MAJOR 5.7
ENV MYSQL_VERSION 5.7.28-1debian9

VOLUME /var/lib/mysql

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s usr/local/bin/docker-entrypoint.sh /entrypoint.sh # backwards compat
COPY mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 3306 33060
CMD ["mysqld"]
