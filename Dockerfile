FROM centos:6.9
# https://hub.docker.com/r/library/centos/tags/

RUN \
yum update -y && \
yum install -y epel-release && \
yum update -y epel-release && \
rpm -ivh http://mirror.yandex.ru/fedora/russianfedora/russianfedora/free/el/releases/6/Everything/x86_64/os/puias-release-6-2.R.noarch.rpm && \
rpm --import http://rpms.famillecollet.com/RPM-GPG-KEY-remi && \
rpm -ivh http://rpms.famillecollet.com/enterprise/remi-release-6.rpm && \
yum update -y remi-release && \
yum install -y vim git ntp crontabs gcc && \
yum install -y openssh-server openssh-clients autossh && \
yum install -y libevent-devel gettext-devel libmcrypt-devel mcrypt libyaml-devel && \
yum install -y openssl-devel libffi-devel && \
yum install -y python27-devel python27-tools python27-setuptools python27-pip && \
pip2.7 install --upgrade pip && \
/bin/cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
mkdir -p /var/log/cto && \
mkdir -p /etc/supervisord.d && \
mkdir -p /etc/cto.d && \
git clone --depth=1 -b latest git@github.com:cto-tamagoya/tamagoya-py.git /var/cto && \
/bin/bash -c "cd /var/cto && pip install -r /var/cto/requirements.txt" && \
yum clean all

# CMD ["/usr/bin/supervisord"]
CMD /bin/bash /var/cto/script/docker.start.sh
