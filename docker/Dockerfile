FROM ubuntu:18.04
LABEL maintainer="yangx.a.zhou@intel.com"

# environment variables
ENV http_proxy http://10.239.4.80:913
ENV https_proxy http://10.239.4.80:913
ENV DEBIAN_FRONTEND noninteractive
ENV PATH /depot_tools:$PATH
ENV NO_AUTH_BOTO_CONFIG /home/user/work/awfy/docker/.boto
ENV WORKHOME /home/user/work

# install related packages
RUN apt-get update && apt-get install -y vim rsync python python-pip python-mysqldb python-tornado git curl mysql-client-5.7 expect wget tzdata software-properties-common && \
    LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/php && LC_ALL=C.UTF-8 add-apt-repository -y ppa:ondrej/apache2 && \
    apt-get update && apt-get install -y apache2 php5.6 php5.6-mysql

# download depot_tools
RUN cd / && git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git && update_depot_tools

# download awfy scripts
RUN mkdir /repos /logs && mkdir -p /home/user/work && cd /home/user/work && ln -s /repos && ln -s /logs && \
    git clone https://<YOUR_GITLAB_USERNAME>:<YOUR_GITLAB_PASSWORD>@gitlab.devtools.intel.com/zhouy7x/awfy.git
#    && cd awfy && python replace_host.py  ssgs5-test.sh.intel.com  `hostname -s`
#RUN git submodule update --init --recursive

# set apache2 config
ADD apache2.conf /etc/apache2/apache2.conf
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
ADD ports.conf /etc/apache2/ports.conf

VOLUME /repos
VOLUME /logs

# run
WORKDIR $WORKHOME
EXPOSE 8000 7777
CMD ["/bin/bash"]
