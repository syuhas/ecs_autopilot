job('fetch_subdomains') {
    description('Freestyle job to fetch existing subdomains in selected AWS accounts.')

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
chmod +x deploy/fetch_jobs/subdomains.sh
./deploy/fetch_jobs/subdomains.sh
        ''')
    }
}
