# About

Scripts used by CirleCi, build to setup access to the test/demo host -- or any host that is directly configured by CircleCI.

# IAM Requirements

The AWS Credentials must allow use of authorize-security-group-ingress aws cli command, at minimum

List of credentials as I determine them

    authorize-security-group-ingress
    describe-security-groups
    revoke-security-group-ingress


# Deploy Host

The scripts don't work properly on an auto-scaling group type setup, as they require a static host.

I could use some AWS commands to query the host, but not going to bother with that right now. Hence, the "DEPLOY_HOST" environment variable needs to be setup in CircleCI environment variables.

