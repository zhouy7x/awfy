FROM ubuntu:18.04
LABEL maintainer="yangx.a.zhou@intel.com"

# environment variables
ENV http_proxy http://10.239.120.56:913
ENV https_proxy http://10.239.120.56:913
ENV DEBIAN_FRONTEND noninteractive
ENV PATH $PATH:/depot_tools
ENV NO_AUTH_BOTO_CONFIG /home/user/work/awfy/docker/.boto
ENV WORKHOME /home/user/work/awfy/driver

# install related packages
RUN apt-get update && apt-get install -y vim rsync python python-pip python3-pip python-mysqldb python-tornado git curl \
    mysql-client-5.7 expect wget tzdata software-properties-common sshpass && python -m pip install subprocess32 && \
    LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/php && LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/apache2 && \
    apt-get update && apt-get install -y apache2 libapache2-mod-php5.6 php5.6 php5.6-gd php5.6-mysql php5.6-xsl

# install locale en_US.utf8
RUN apt-get clean && apt-get update && apt-get install -y locales && locale-gen en_US.utf8 && update-locale
ENV LANG en_US.UTF-8

# download depot_tools
RUN cd / && git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git && update_depot_tools

# create source path
RUN mkdir /repos /logs /awfy && mkdir -p /home/user/work && cd /home/user/work && ln -s /repos && ln -s /logs && \
    ln -s /awfy

# set timezone to Asia/Shanghai
RUN rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# set apache2 config
ADD apache2.conf /etc/apache2/apache2.conf
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
ADD ports.conf /etc/apache2/ports.conf

VOLUME /repos
VOLUME /logs
VOLUME /awfy

# run
WORKDIR $WORKHOME
#ENTRYPOINT ["./all_run.py"]
EXPOSE 8000 7777
CMD ["./all_run.py"]
