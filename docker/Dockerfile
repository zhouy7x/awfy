FROM ubuntu:18.04
LABEL maintainer "zhouy7x@gmail.com"


# set proxy
ENV http_proxy http://10.239.4.80:913
ENV https_proxy http://10.239.4.80:913

# install related packages
RUN apt-get update && apt-get install -y vim rsync python python-pip python-mysqldb tornado apache2 git expect software-properties-common && \
    add-apt-repository ppa:ondrej/php && apt-get install -y php5.6 php5.6-mysql

# download depot_tools
RUN cd / && git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

# environment variables
ENV PATH /depot_tools:$PATH
ENV NO_AUTH_BOTO_CONFIG /home/user/work/awfy/docker/.boto
ENV WORKHOME /home/user/work

# download awfy scripts
RUN mkdir /repos /logs && mkdir -p /home/user/work && cd /home/user/work && ln -s /repos && ln -s /logs && \
    git clone https://gitlab.devtools.intel.com/zhouy7x/awfy.git && cd awfy && git submodule update --init --recursive && \
    python replace_host.py  ssgs5-test.sh.intel.com  `hostname -s`

# set apache2 config
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
ADD ports.conf /etc/apache2/ports.conf
ADD .ssh /root/.ssh

# run
WORKDIR $WORKHOME
EXPOSE 8000
EXPOSE 7777
CMD ["/bin/bash"]