#!/usr/bin/env bash

iptables -I DOCKER -p tcp --dport 3306 -j DROP 
iptables -I DOCKER -p tcp --dport 3306 -d 127.0.0.1/8 -j ACCEPT
iptables -I DOCKER -p tcp --dport 3306 -d 172.17.0.1/16 -s 127.0.0.1/8 -j ACCEPT
iptables -I DOCKER -p tcp --dport 3306 -d 172.17.0.1/16 -s 213.190.22.172/32 -j ACCEPT
iptables -I DOCKER -p tcp --dport 3306 -d 213.190.22.172/32 -s 172.17.0.1/16 -j ACCEPT

iptables -I INPUT -p tcp --dport 3306 -j DROP
iptables -I INPUT -p tcp --dport 3306 -d 127.0.0.1/8 -j ACCEPT
