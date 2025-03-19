<p align="center">
  <img src="https://s3.us-east-1.amazonaws.com/www.digitalsteve.net/aplogo.png" alt="Diagram">
</p>

# ECS AutoPilot


## Getting Started
### **Prerequisites**

Autopilot requres some initial setup of infrastructure, roles and a working Jenkins server with provisioned cloud nodes. For a more detailed breakdown of the prerequisites, visit https://digitalsteve.net/projects/jenkins-ecs?tab=Prerequisites.

### **How It Works**

AutoPilot uses a centralized configuration and requires
![structure](https://github.com/user-attachments/assets/0024982b-9087-477a-962c-ed33d836d490)

### Installation
**Clone the Repository:**
```sh
git clone https://github.com/syuhas/websitev2.git
cd websitev2
```

**Install Dependencies**
```sh
npm install
```
> Note: This project uses a customized script and style from from the base [PrismJS](https://github.com/PrismJS/prism) package to mimic VSCode highlighting for Python (`npm install @syuhas22/prismjs`)
> Backup custom styles can be found in ./deploy/prism_custom/

**Check Version Against Listed Versions**
```sh
npx ng version
```
...or if CLI is installed globally...
```sh
ng version
```
**Running the Development Server**
Run for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.
```sh
npx ng serve
```
...or if CLI is installed globally...
```sh
ng serve
```
