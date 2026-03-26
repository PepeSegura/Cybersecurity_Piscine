#!/bin/bash

echo "Starting ft_onion container"
echo "========================================="

mkdir -p /var/lib/tor/hidden_nginx /var/lib/tor/hidden_ssh
chown -R debian-tor:debian-tor /var/lib/tor
chmod 700 /var/lib/tor/hidden_nginx /var/lib/tor/hidden_ssh

service ssh start
service nginx start
service tor start

echo "Waiting for services to start"
sleep 15

if [ -f /var/lib/tor/hidden_nginx/hostname ]; then
    echo -n "nginx_tor: "
    cat /var/lib/tor/hidden_nginx/hostname
fi

if [ -f /var/lib/tor/hidden_ssh/hostname ]; then
    echo -n "ssh_tor: "
    cat /var/lib/tor/hidden_ssh/hostname
fi

echo "All services running."
echo "========================================="


tail -f /dev/null
