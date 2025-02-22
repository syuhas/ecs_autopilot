import boto3
import json
import os
import re
from loguru import logger
import yaml

# list all subdomains ending in domain 'digitalsteve.net' for all accounts in the list
workspace = os.environ['WORKSPACE']
jenkins_home = os.environ['JENKINS_HOME']
file_path = os.path.join(workspace, 'subdomains.json')
# add role name here. role should have the same name in all accounts and should have the same permissions
cross_account_role = 'jenkinsAdminXacnt'
# add your accounts here
accounts = [
    "551796573889",
    "061039789243"
]

def assume_role_session(account):
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=f"arn:aws:iam::{account}:role/jenkinsAdminXacnt",
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
                        # trimmed_name = record_set['Name'][:-1]
                        identity = session.client('sts').get_caller_identity()
                        # regex = re.compile(r'^((?!digitalsteve\.)[^.]+\.)+(?=digitalsteve\.net$)')
                        # match = regex.search(trimmed_name)
                        # if match:
                        #     trimmed_subdomain = match.group()[:-1]
                        #     logger.info(f'{trimmed_subdomain} ({trimmed_name}) ({identity["Account"]})')
                        #     domains.append(f'{trimmed_subdomain} ({trimmed_name}) ({identity["Account"]})')
                        name = record_set['Name']
                        domains.append(f'{name} ({identity["Account"]})')
                        
                        
    return domains
                        
    

subdomains = []
for account in accounts:
    session = assume_role_session(account)
    subdomains += get_subdomains(session)


# write subdomains to a json file

with open(file_path, 'w') as f:
    json.dump(subdomains, f)

print(f"Subdomains saved to: {file_path}")
    
# make the github directory if it doesnt exist
os.makedirs(f'{jenkins_home}/github', exist_ok=True)

with open(f'{jenkins_home}/github/subdomains.json', 'w') as f:
    json.dump(subdomains, f)
    
print(f"Subdomains saved to: /home/jenkins_home/github/subdomains.json")