from typer import Typer


app = Typer()
@app.command()
def config():
    print('Generating config.yaml')
    region = input('Enter the region: ')
    app_name = input('Enter the app name: ')
    num_accounts = int(input('Enter the number of accounts: '))
    accounts = {}
    for i in range(num_accounts):
        account_id = input('Enter the account id: ')
        security_group = input('Enter the security group: ')
        subnet_ids = input('Enter the subnet ids(separate multiple subnets with commas): ').split(',')
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
            'subnet_ids': subnet_ids,
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

    # write the config.yaml file
    with open('config.yaml', 'w') as f:
        f.write(f'region: "{region}"\n')
        f.write(f'app_name: "{app_name}"\n')
        f.write('aws_accounts:\n')
        for account_id, account in accounts.items():
            f.write(f'  "{account_id}":\n')
            for key, value in account.items():
                f.write(f'    {key}: "{value}"\n')
    print('config.yaml file generated')
    
if __name__ == '__main__':
    app(prog_name='config')