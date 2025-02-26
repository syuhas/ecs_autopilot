from typer import Typer, Argument
from typing_extensions import Annotated
import yaml
from loguru import logger


app = Typer()
def print_logo():
    logo = """
 _______________________________________________________________________
|\                                                                       \\
| |***********************************************************************|
| |*                                                                     *|
| |*         ./^$$$$        ./^$$   $$  .|^$$$$$$$$     ./^$$$           *|
| |*        ./ $$  $$       .| $$   $$   .\   $$      ./ $$   $$         *|
| |*       ./ $$    $$      .| $$   $$     .| $$     .| $$     $$        *|
| |*      ./ $$$$$$$$$$     .| $$   $$     .| $$     .| $$     $$        *|
| |*     ./ $$$      $$$    .| $$   $$     .| $$      .\ $$   $$         *|
| |*    ./ $$$        $$$   .| $$$$$$$     .| $$       .\  $$$           *|
| |*   .|___/       /__/    .|_______|     .|___/       .\__/            *|
| |*                                                                     *|
| |*  .|^$$$$$$$$$    .|^$$     .|^$$         ./^$$$      .|^$$$$$$$$    *|
| |*  .| $$      $$   .| $$     .| $$       ./ $$   $$     .\   $$       *|
| |*  .| $$      $$   .| $$     .| $$      .| $$     $$      .| $$       *|
| |*  .| $$$$$$$$$    .| $$     .| $$      .| $$     $$      .| $$       *|
| |*  .| $$           .| $$     .| $$       .\ $$   $$       .| $$       *|
| |*  .| $$           .| $$     .| $$$$$$$   .\  $$$         .| $$       *|
| |*  .|__/           .|__/     .|______|     .\__/          .|___/      *|
| |*                                                                     *|
| |*                   +---------------------------+                     *|
| |*                   |                           |                     *|
| |*                   |          __|__            |                     *|
| |*                   |    ----@--(_)--@----      |                     *|
| |*                   |                           |                     *|
| |*                   |          Yaml             |                     *|
| |*                   |         Config            |                     *|
| |*                   |        Generator          |                     *|
| |*                   +---------------------------+                     *|
 \|_______________________________________________________________________|           
            """                                  
    print(logo)

#     """
#     print(logo)

@app.command()
def config(accounts_num: Annotated[int, Argument(help="Number of accounts")] = 1):
    print('\n')
    print_logo()
    if accounts_num < 1 or accounts_num > 10:
        raise Exception('Please enter between 1-10 accounts')
    if accounts_num == 1:
        print('', '_'*73, '')
        print('|', ' '*71, '|')
        print(f"|                 Generating 'config.yaml' for {accounts_num} account...               |")
        print('|', ' '*71, '|')
        print('|_________________________________________________________________________|')
    else:
        print('', '_'*73, '')
        print('|', ' '*71, '|')
        print(f"|                 Generating 'config.yaml' for {accounts_num} accounts...              |")
        print('|', ' '*71, '|')
        print('|_________________________________________________________________________|')
    print('\n')
    region = input('Region: ')
    app_name = input('Enter a name for your app: ')
    accounts = {}
    for i in range(accounts_num):
        print('\n')
        print('', '_'*73, '')
        print('|', ' '*71, '|')
        print(f"|                    Account #{i+1} Details:                                  |")
        print('|', ' '*71, '|')
        print('|_________________________________________________________________________|')
        print('\n')
        account_id = input(f'Account ID {i+1}: ')
        security_group = input('Primary Security Group: ')
        subnet_ids = input('Subnet IDs(separate multiple subnets with commas): ')
        vpc_id = input('VPC ID: ')
        tf_bucket = input('Terraform Lock File Bucket: ')
        tf_table = input('Terraform Lock File DynamoDB Table: ')
        ssl_certificate_arn = input('SSL Certificate ARN (for registered domain): ')
        route53_zone_id = input('Route53 Zone ID(for regisered domain): ')
        domain = input('Domain Name(eg. example.com): ')
        cross_account_role = input('Cross Account Role Name (Only the role name; Should be uniform across accounts): ')
        execution_role = input('ECS Task Execution Role(Should be uniform across accounts): ')
        task_role = input('Enter the Task Role (To Enable ECSExec; Should be uniform across accounts): ')
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
    with open('deploy/fetch_jobs/config.yaml', 'w') as file:
        yaml.dump(account_data, file, default_flow_style=False)
    print('\n')
    print('config.yaml generated successfully')
    print('\n')
    
if __name__ == '__main__':
    app(prog_name='config')