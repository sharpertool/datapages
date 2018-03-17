#!/usr/bin/env bash

# Use an environment variable which works locally, but then on CircleCI use the global, default environment.
profilename=${BIGZETA_AWS_PROFILE:-''}
if [ ! -z "${profilename}" ]
then
    export profile="--profile ${profilename}"
else
    export profile=''
fi

# Security group with inbound ssh access to target server.
export sgname=${BIGZETA_CIRCLECI_SG:-sg-78f1e707}

