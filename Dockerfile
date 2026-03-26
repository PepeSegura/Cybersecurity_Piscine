FROM debian:latest

RUN apt-get update -y && apt upgrade -y
RUN apt-get install nginx tor openssh-server -y

COPY config/sshd_config     /etc/ssh/sshd_config
COPY config/torrc           /etc/tor/torrc
COPY config/nginx.conf      /etc/nginx/nginx.conf
COPY config/index.html      /usr/share/nginx/html/index.html

RUN useradd -m ft_onion && echo "ft_onion:ft_onion" | chpasswd

COPY config/entrypoint.sh   /config/entrypoint.sh
RUN chmod +x /config/entrypoint.sh
CMD ["/config/entrypoint.sh"]
