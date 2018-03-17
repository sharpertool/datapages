#!/usr/bin/env bash

host="Host deploy_host"
nm="  Hostname ${DEPLOY_HOST}"
user="  User ec2-user"
strict="  StrictHostKeyChecking no"
proxy="  ProxyCommand ssh -q ${BASTION} nc %h %p"

mkdir -p ~/.ssh
echo -e "Host ${BASTION}\n  StrictHostKeyChecking no\n\n" >> ~/.ssh/config
echo -e "${host}\n${nm}\n${user}\n${strict}\n${proxy}\n\n" >> ~/.ssh/config

cat ~/.ssh/config




