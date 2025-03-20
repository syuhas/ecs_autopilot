# ECS AutoPilot
<p align="center">
  <img src="https://github.com/user-attachments/assets/3afe29fe-dfa2-4da7-8794-44e6437bbaff" alt="Diagram">
</p>


## **How It Works**

![jenkinsworkflow](https://github.com/user-attachments/assets/84bb86c1-c375-463f-b005-839aa72d2ad6)

**AutoPilot uses a centralized pipeline and configuration to deploy all of your Dockerized applications to AWS ECS.**

### 1. Prepare Your Application
- Use the provided tools to generate a *config.yaml* file (or fill out manually) and copy it to your application repository (in the *deploy/docker* directory)
- Ensure a valid Dockerfile is present at the root of your application repository.

### 2. Generate AutoPilot Jobs
- Install AutoPilot Locally and run command to generate the DSL script
- Create the seed jobs in Jenkins and run them to create the AutoPilot pipeline and fetch jobs

### 3. Run the Fetch Jobs to Populate the Job Parameter Dropdown
- Execute the Fetch Repositories & Branches job to retrieve available repositories.
- Execute the Fetch Subdomains job to load available domains from AWS Route 53.

### 4. Start the Deployment Pipeline
- In Jenkins, run the AutoPilot pipeline with the following parameters:
  - ✅ Repository & Branch – Select the GitHub repository and branch to deploy.
  - ✅ Account - Choose the AWS account to deploy to.
  - ✅ Subdomain – Enter the subdomain for deployment.
  - ✅ Deployment Option:
    - *Deploy* – Creates a fresh deployment, replacing existing infrastructure.
    - *Update* – Deploys a new image while keeping existing infrastructure.
    - *Destroy* – Removes all resources for the subdomain.
    - *Test* - Dry run the environment variables and parameters for you job.

### 5. Deploy Your Application
- AutoPilot provisions infrastructure and deploys your application to ECS.
- The subdomain is configured, and your application is live! 🚀

## Getting Started
### **Prerequisites**

Autopilot requres some initial setup of infrastructure, roles and a working Jenkins server with provisioned cloud nodes. 
- A Jenkins server with the required plugins installed ([Active Choices, Pipeline: Groovy, Git, Job DSL, Credentials Binding, Pipeline Utility])
- A GitHub account to store application repositories
- A GitHub personal access token stored as GITHUB_TOKEN in Jenkins credentials for API access
- AWS IAM roles configured to assume deployment permissions
- A Route 53 domain with a hosted zone
- An SSL certificate for HTTPS connections (issued via ACM)
- A VPC, Subnets, and Security Groups for deployment
- An S3 bucket and DynamoDB table for Terraform state management

For a more detailed breakdown of the prerequisites, visit the [Prerequisites Guide](https://digitalsteve.net/projects/jenkins-ecs?tab=Prerequisites) here.



## Installation
**Fork and Clone the Repository:**
```sh
git clone https://github.com/YOUR_USERNAME/ecs_autopilot.git
cd ecs_autopilot
```

**Set Up a Virtual Environment:**
```sh
pip install python3-venv
python -m venv venv
source venv/bin/activate  # (For Windows: venv\Scripts\activate)
```

**Upgrade pip and install dependencies:**
```sh
pip install -U pip
pip install -e .
```

## Configuration YAML Setup
![image](https://github.com/user-attachments/assets/e6a94e46-819f-46ce-abb7-a982d45725f9)

AutoPilot provides two ways to generate a configuration file:

- **Textual UI:**
```sh
config_ui
```
  This will launch an interactive UI to guide you through configuration.

- **Command Line:**
```sh
config
```
  This will launch an interactive command line to guide you through configuration.

(The config file may also be filled out manually. These tools are provided for convenience.)


## Jenkins Job Setup
### Generate Seed DSL Scripts
With your *config.yml* generated, run:
```sh
config_dsl
```
This will generate Job DSL scripts needed to set up the Jenkins seed jobs.

![dsls](https://github.com/user-attachments/assets/3f5f797b-cf03-4994-8402-1138f7963adc)


### Create Jenkins Seed Jobs
Log in to your Jenkins Server:
- Create a *Freestyle Job* for each DSL script and name them whatever you want.
- Under *Source Code Management*, enter your forked AutoPilot repository URL.
- Add *Process Job DSLs* and for each job, enter the location of the script.
  - *dsl/seed_job_ecs_deployer.groovy*
  - *dsl/seed_job_fetch_repos.groovy*
  - *dsl/seed_job_fetch_subdomains.groovy*

[For detailed steps, follow the [seed jobs guide](https://digitalsteve.net/projects/jenkins-ecs?tab=Seed%20Jobs).]

Run Each Seed job to create the main pipeline and fetch jobs.


### Fetch Repository and Subdomain Data
Once the seed jobs are created, run the following Jenkins jobs:
✅ Fetch Repositories & Branches – Retrieves repository and branch names from GitHub.
✅ Fetch Subdomains – Retrieves active subdomains from AWS Route 53.

Running these will populate the Active Choice Parameters dropdown and subdomains in the main pipeline job.
(Note: Jenkins will require script approvals before running these jobs.)


## Prepare Your Application
### Add Required Files to Your Repository

Ensure your application repository contains the following files:

📂 deploy/docker/

config.yaml (Generated configuration file)

📂 deploy/scripts/

Any additional bash or Python scripts needed for setup

📂 Root Directory

Dockerfile (Required for ECS deployment)

![files_structure](https://github.com/user-attachments/assets/fa1ad6fe-c022-4261-b937-8fbb0085a0cf)

## Run the Pipeline

- Click *Build Now*, select your job parameters, and run the application.

![image](https://github.com/user-attachments/assets/7fe61ac4-f935-47e8-9c33-b4d85d6548c7)

- You Application Will now be Live on the Selected Subdomain! 
