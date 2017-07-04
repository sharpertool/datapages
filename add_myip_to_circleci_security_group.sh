#!/usr/bin/env bash

source ./getenv_circleci_security_group.sh

public_ip_address=$(wget -qO- http://checkip.amazonaws.com)
cidr="${public_ip_address}/32"
port=22

echo "Adding access to port ${port} to ${cidr} in SG ${sgname}."

aws ec2 ${profile} authorize-security-group-ingress \
    --region us-west-2 --group-id ${sgname} \
    --protocol tcp \
    --port 22   \
    --cidr ${cidr}

