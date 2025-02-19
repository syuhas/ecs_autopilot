pipelineJob('test_ecs-deployer') {
    description('Pipeline job to deploy repositories with Active Choice Parameters.')

    // General configurations
    parameters {
        choiceParameter {
            name('Repository')
            description('Select a repository to deploy')
            choiceType('PT_SINGLE_SELECT') // Single selection dropdown

            script {
                groovyScript {
                    script("""
                        import groovy.json.JsonSlurper
                        def jenkinsHome = System.getenv("JENKINS_HOME")
                        def jsonFile = new File("${jenkinsHome}/github/github_branches.json")
                        if (!jsonFile.exists()) {
                            return ["No Repositories Found"]
                        }
                        def jsonContent = new JsonSlurper().parseText(jsonFile.text)
                        return jsonContent.keySet().toList()
                    """)
                    sandbox(false)
                }
                fallbackScript {
                    script("return ['No Repositories Available']")
                    sandbox(true)
                }
            }
        }

        choiceParameter {
            name('Branch')
            description('Select a branch for the selected repository')
            choiceType('PT_RADIO') // Radio button selection
            referencedParameters(['Repository'])

            script {
                groovyScript {
                    script("""
                        import groovy.json.JsonSlurper
                        def jenkinsHome = System.getenv("JENKINS_HOME")
                        def jsonFile = new File("${jenkinsHome}/github/github_branches.json")
                        if (!jsonFile.exists()) {
                            return ["No Branches Found"]
                        }
                        def jsonContent = new JsonSlurper().parseText(jsonFile.text)
                        def branches = jsonContent[Repository] ?: ["No Branches Found"]
                        return branches
                    """)
                    sandbox(false)
                }
                fallbackScript {
                    script("return ['No Branches Available']")
                    sandbox(true)
                }
            }
        }

        choiceParam('Options', ['Deploy', 'Update', 'Destroy', 'DestroyECR'], 'Select an operation.')
        choiceParam('Account', ['551796573889', '061039789243'], 'Select an AWS account.')
        stringParam('Subdomain', 'test', 'Subdomain to deploy (eg. php = php.example.net or php.dev.example.net).')

        choiceParameter {
            name('Subdomains Currently In Use')
            description('List of subdomains currently in use')
            choiceType('PT_MULTI_SELECT') // Allows multiple selections

            script {
                groovyScript {
                    script("""
                        import groovy.json.JsonSlurper
                        def filePath = "/home/jenkins_home/workspace/fetch_subdomains/subdomains.json"
                        def subdomainsList = []
                        if (new File(filePath).exists()) {
                            def jsonText = new File(filePath).text
                            subdomainsList = new JsonSlurper().parseText(jsonText)
                        }
                        if (subdomainsList.isEmpty()) {
                            return ["No subdomains currently in use."]
                        } else {
                            return subdomainsList
                        }
                    """)
                    sandbox(false)
                }
                fallbackScript {
                    script("return ['No Subdomains Available']")
                    sandbox(true)
                }
            }
        }
    }

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        url('https://github.com/syuhas/ecs_deployer')
                    }
                    branch('*/main')
                }
            }
            scriptPath('deploy/docker/Jenkinsfile')
            lightweight(true)
        }
    }
}
