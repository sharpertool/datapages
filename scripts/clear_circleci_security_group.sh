#!/usr/bin/env bash

mypath=$(dirname $0)

source ${mypath}/getenv_circleci_security_group.sh

current_security_group=$(aws ec2 ${profile} describe-security-groups --region us-west-2 --group-id ${sgname})
ip_count=$(echo ${current_security_group} | jq -r '.SecurityGroups[0].IpPermissions | length')
if [ ${ip_count} > 0 ]; then
    for (( n=0; n < $ip_count; n++ ))
    do
        this_port=$(echo ${current_security_group} | jq -r ".SecurityGroups[0].IpPermissions[${n}].FromPort")
        cidr_count=$(echo ${current_security_group} | jq -r ".SecurityGroups[0].IpPermissions[${n}].IpRanges | length")
        for (( c=0; c < $cidr_count; c++ ))
        do
            this_cidr=$(echo ${current_security_group} | jq -r ".SecurityGroups[0].IpPermissions[${n}].IpRanges[${c}].CidrIp")
            echo "Revoke ${this_cidr} in SG ${sgname}"
            aws ec2 ${profile} revoke-security-group-ingress --region us-west-2 --group-id ${sgname} --protocol tcp --port ${this_port} --cidr ${this_cidr}
        done
    done
fi
