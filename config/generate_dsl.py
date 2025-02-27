import yaml
from jinja2 import Environment, FileSystemLoader


def app():

    # Load the YAML configuration file
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Extract the AWS accounts
    aws_accounts = config.get('aws_accounts', [])
    giturl = config.get('autopilot_repo', '')

    # Set up Jinja2 environment to load templates
    env = Environment(loader=FileSystemLoader('dsl/jinja'))  # Assuming templates are in the 'templates' directory
    template_ecs_autopilot = env.get_template('seed_job_ecs_deployer.groovy.jinja')
    template_fetch_repos = env.get_template('seed_job_fetch_repos.groovy.jinja')
    template_fetch_subdomains = env.get_template('seed_job_fetch_subdomains.groovy.jinja')

    # Render the template with the AWS accounts
    rendered_autopilot = template_ecs_autopilot.render(aws_accounts=aws_accounts, autopilot_repo=giturl)
    rendered_repos = template_fetch_repos.render(autopilot_repo=giturl)
    rendered_subdomains = template_fetch_subdomains.render(autopilot_repo=giturl)
    

    # Write the generated DSL script to a file
    with open('dsl/seed_job_ecs_deployer.groovy', 'w') as f:
        f.write(rendered_autopilot)

    with open('dsl/seed_job_fetch_repos.groovy', 'w') as f:
        f.write(rendered_repos)
    with open('dsl/seed_job_fetch_subdomains.groovy', 'w') as f:
        f.write(rendered_subdomains)
    
    print("DSL Jobs Generated Successfully!")
    print('Jobs generated: \n')
    print('\tdsl/seed_job_ecs_deployer.groovy')
    print('\tdsl/seed_job_fetch_repos.groovy')
    print('\tdsl/seed_job_fetch_subdomains.groovy')
    print('\n')
    
if __name__ == '__main__':
    app()