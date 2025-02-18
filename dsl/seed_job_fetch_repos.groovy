job('fetch_repos') {
    description('Freestyle job to fetch GitHub repos and list branches.')

    // Restrict the job to run only on the built-in node
    label('built-in')

    // Source Code Management (SCM) - Git
    scm {
        git {
            remote {
                url('https://github.com/syuhas/ecs_deployer.git')
            }
            branch('*/main')
        }
    }

    // Build Triggers - Only runs when deploy-repos is built
    // triggers {
    //     upstream('deploy-repos', 'SUCCESS')
    // }

    // Inject Environment Variables using CloudBees Credentials Plugin
    wrappers {
        credentialsBinding {
            string('TOKEN', 'GITHUB_TOKEN')  // Replace with actual credential ID
        }
    }

    // Build Steps - Run the shell script
    steps {
        shell('''
            #!/bin/bash
            chmod +x deploy/fetch_jobs/repos.sh
            ./deploy/fetch_jobs/repos.sh
        ''')
    }
}
