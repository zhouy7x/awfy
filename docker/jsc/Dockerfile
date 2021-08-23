FROM ubuntu:20.04
LABEL maintainer="yangx.a.zhou@intel.com"

# environment variables
ENV http_proxy http://10.239.4.100:913
ENV https_proxy http://10.239.4.100:913
ENV DEBIAN_FRONTEND noninteractive
ENV WORKHOME /awfy/driver

# install related packages
RUN apt-get update && \
    apt-get install -y git libicu-dev python-is-python2 ruby bison flex cmake build-essential ninja-build git gperf \
    ssh rsync lsof && apt-get clean

ADD .ssh /root/.ssh
# create source path
RUN mkdir /repos /awfy /logs && mkdir -p /home/user/work && cd /home/user/work && ln -s /repos && ln -s /awfy \
    && ln -s /logs && mkdir -p /var/run/sshd && mkdir -p /run/sshd
VOLUME /repos
VOLUME /awfy
VOLUME /logs

# run
WORKDIR $WORKHOME
#ENTRYPOINT ["./build_server.py"]
EXPOSE 8912 22
CMD ["/bin/bash"]
