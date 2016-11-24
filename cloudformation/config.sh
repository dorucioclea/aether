#!/usr/bin/env bash

stack_name="gather2"
billing_project='gather2'
hosted_zone_name="ehealthafrica.org"
ssh_key_name="aws-deploy"
cf_s3_bucket="eha-cloudformation"
cf_s3_zip_file="example-docker.zip"
rename_lambda="arn:aws:lambda:eu-west-1:387526361725:function:rename_resources"
get_or_create_record_lambda="arn:aws:lambda:eu-west-1:387526361725:function:get_or_create_record"
sns_topic="arn:aws:sns:eu-west-1:387526361725:slack_notification"
ssl_cert="arn:aws:acm:eu-west-1:387526361725:certificate/b093a099-e453-4290-90b4-8a97f43174ec"
image_id="ami-bdee9dce"
