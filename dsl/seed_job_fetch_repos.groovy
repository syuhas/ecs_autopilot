job('test_fetch_repos') {
    description('Fetches repositories from GitHub and lists branches')
    // Enter your own Github user and token parameters
    parameters {
        stringParam('GITHUB_USER', 'syuhas', 'GitHub organization or user from which to fetch repositories')
    }

    environmentVariables {
        env('TOKEN', credentials('GITHUB_TOKEN'))
    }

    steps {
        shell('''
            #!/bin/bash

            chmod +x deploy/fetch_jobs/subdomains.sh

            ./deploy/fetch_jobs/subdomains.sh
        ''')
    }
}