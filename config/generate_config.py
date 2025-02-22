from typer import Typer, Argument
from typing_extensions import Annotated
import yaml
from loguru import logger


app = Typer()
@app.command()
def config(accounts_num: Annotated[int, Argument(help="Number of accounts")] = 1):
    print('\n')
    if accounts_num < 1 or accounts_num > 10:
        raise Exception('Please enter between 1-10 accounts')
    if accounts_num == 1:
        print(f'Generating config.yaml for {accounts_num} account...')
    else:
        print(f'Generating config.yaml for {accounts_num} accounts...')
    print('\n')
    region = input('Enter the region: ')
    app_name = input('Enter the app name: ')
    accounts = {}
    for i in range(accounts_num):
        print('\n')
        logger.info(f'Account {i+1}')
        print('\n')
        account_id = input(f'Enter the account id for account {i+1}: ')
        security_group = input('Enter the security group: ')
        subnet_ids = input('Enter the subnet ids(separate multiple subnets with commas): ')
        vpc_id = input('Enter the vpc id: ')
        tf_bucket = input('Enter the tf bucket: ')
        tf_table = input('Enter the tf table: ')
        ssl_certificate_arn = input('Enter the ssl certificate arn: ')
        route53_zone_id = input('Enter the route53 zone id: ')
        domain = input('Enter the domain: ')
        cross_account_role = input('Enter the cross account role: ')
        execution_role = input('Enter the execution role: ')
        task_role = input('Enter the task role: ')
        accounts[account_id] = {
            'security_group': security_group,
            'subnet_ids': subnet_ids.split(','),
            'vpc_id': vpc_id,
            'tf_bucket': tf_bucket,
            'tf_table': tf_table,
            'ssl_certificate_arn': ssl_certificate_arn,
            'route53_zone_id': route53_zone_id,
            'domain': domain,
            'cross_account_role': cross_account_role,
            'execution_role': execution_role,
            'task_role': task_role,
        }
        account_data = {
            'region': region,
            'app_name': app_name,
            'aws_accounts': accounts
        }
    with open('config.yaml', 'w') as file:
        yaml.dump(account_data, file, default_flow_style=False)
    with open('fetch_jobs/config.yaml', 'w') as file:
        yaml.dump(account_data, file, default_flow_style=False)
    print('\n')
    print('config.yaml generated successfully')
    print('\n')
    
if __name__ == '__main__':
    app(prog_name='config')