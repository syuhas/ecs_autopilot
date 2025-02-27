import groovy.yaml.YamlSlurper

pipelineJob('test_ecs-deployer') {
    description('Pipeline job to deploy repositories with Active Choice Parameters.')

    parameters {
        activeChoiceParam('Repository') {
            description('Select a repository.')
            choiceType('SINGLE_SELECT')
            groovyScript {
                script('''
import groovy.json.JsonSlurper
def jenkinsHome = System.getenv("JENKINS_HOME")
def jsonFile = new File("${jenkinsHome}/github/github_branches.json")
if (!jsonFile.exists()) {
    return ["No Repositories Found"]
}
def jsonContent = new JsonSlurper().parseText(jsonFile.text)
return jsonContent.keySet().toList()
                ''')
            }
        }

        activeChoiceReactiveParam('Branch') {
            description('Select a branch based on the repository.')
            choiceType('RADIO')
            referencedParameter('Repository')
            groovyScript {
                script('''
import groovy.json.JsonSlurper
def jenkinsHome = System.getenv("JENKINS_HOME")
def jsonFile = new File("${jenkinsHome}/github/github_branches.json")
if (!jsonFile.exists()) {
    return ["No Branches Found"]
}
def jsonContent = new JsonSlurper().parseText(jsonFile.text)
def branches = jsonContent[Repository] ?: ["No Branches Found"]
return branches

                ''')
            }
        }

        choiceParam('Options', ['Deploy', 'Update', 'Destroy', 'Test'], 'Select an operation.')
        // update with your own AWS account numbers
        def config = new File("config/config.yaml")
        def yaml = new YamlSlurper().parse(config)
        def aws_accounts = yaml.aws_accounts
        choiceParam('Account', aws_accounts, 'Select an AWS account.')
        stringParam('Subdomain', 'myapp', 'Subdomain to deploy (eg. php = php.example.net or php.dev.example.net).')

        activeChoiceParam('Subdomains Currently In Use') {
            description('Displays currently used subdomains.')
            choiceType('MULTI_SELECT')
            groovyScript {
                script('''
import groovy.json.JsonSlurper
def filePath = "${jenkinsHome}/github/subdomains.json"
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
                ''')
            }
        }
    }

    definition {
        cpsScm {
            scm {
                git {
                    remote {
                        // update with your own repository
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
