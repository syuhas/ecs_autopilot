import boto3
import json
import os
import re
from loguru import logger
import yaml
import json

accounts = []
jenkins_home = os.environ['JENKINS_HOME']

def assume_role_session(account):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account['account_id']}:role/{account['cross_account_role']}",
        RoleSessionName="XacntAssumeRoleSession"
    )
    credentials = assumed_role['Credentials']
    session = boto3.Session(
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    return session

def get_subdomains(session):
    domains = []
    client = session.client('route53')
    paginator = client.get_paginator('list_hosted_zones')
    for page in paginator.paginate():
        for hosted_zone in page['HostedZones']:
            hosted_zone_id = hosted_zone['Id']
            paginator = client.get_paginator('list_resource_record_sets')
            for page in paginator.paginate(HostedZoneId=hosted_zone_id):
                for record_set in page['ResourceRecordSets']:
                    if record_set['Type'] == 'A':
                        identity = session.client('sts').get_caller_identity()
                        name = record_set['Name']
                        domains.append(f'{name} ({identity["Account"]})')
                        
                        
    return domains

# put the account info manually or drop the generated config.yaml file in the fetch_jobs directory
if not os.path.exists('config/config.yaml'):
    logger.info('config.yaml file not found')
    logger.info('Using manual account info...')
    accounts = [
        {
            'account_id': '551796573889',
            'cross_account_role': 'jenkinsAdminXacnt'
        },
        {
            'account_id': '061039789243',
            'cross_account_role': 'jenkinsAdminXacnt'
        }    
    ]
else:
    with open('config/config.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    for acct in config.get('aws_accounts'):
        account_dict = {}
        account_dict['account_id'] = acct
        account_dict['cross_account_role'] = config.get('aws_accounts')[acct].get('cross_account_role')
        accounts.append(account_dict)


                        
    

subdomains = []
for account in accounts:
    session = assume_role_session(account)
    subdomains += get_subdomains(session)

    
# make the github directory if it doesnt exist
os.makedirs(f'{jenkins_home}/github', exist_ok=True)

with open(f'{jenkins_home}/github/subdomains.json', 'w') as f:
    json.dump(subdomains, f)
    
logger.info(f"Subdomains saved to: {jenkins_home}/github/subdomains.json")