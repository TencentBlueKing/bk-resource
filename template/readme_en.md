# Blueapps BkResource Pedestal

## Environment dependencies

1. Based on: python 3.6、MySQL 5.7+、Redis 3.2

2. PIP Source 
    ```
    [global]
    index-url=https://mirrors.tencent.com/repository/pypi/tencent_pypi/simple
    extra-index-url=http://mirrors.cloud.tencent.com/pypi/simple/
    trusted-host = mirrors.tencent.com, mirrors.cloud.tencent.com
    ```   

3. PIP Version

    Require `pip==20.2.3`，declaring the environment variable `PIP_VERSION=20.2.3` in PaaS, and using `pip install --upgrade pip==20.2.3` to install the specified version locally

## Quick Start

### 1. Apply Blueking APP

- Apply Git Repo
- Create Blueking App, and retrieve app_code、app_secret

### 2. Generate Blueapps restful project through cookiecutter

- Refer to [README - Installation](../readme.md#installation)

- Commit
    ```
    cd {app_id}
    git init
    git add .
    git commit -m "minor: init repo"
    git remote add origin {git_url}
    git push -u origin master
    ```

### 3. Deploying development environment according to README.md

## BkResource Framework with 12 Factor

1. [Codebase - One codebase tracked in revision control, many deploys](https://12factor.net/codebase)   
    Manage project code and version easily with Git repository, all services of project can be stored in one repo
2. [Dependencies - Explicitly declare and isolate dependencies](https://12factor.net/dependencies)   
    Declare dependencies in requirements.txt and manage them with PIP
3. [Config - Store config in the environment](https://12factor.net/config)   
    All variable configs are loaded from environment for safe and reusable, `.env` file is also helpful for deploying and migrating services
4. [Backing services - Treat backing services as attached resources](https://12factor.net/backing-services)   
    Using Django ORM or Django Cache Client, MySQL, Redis or other backing services are attached resources
5. [Build, release, run - Strictly separate build and run stages](https://12factor.net/build-release-run)   
    Running stages are seperated by Blueking PaaS, which provides two environment, staging and prodcution, the PaaS build service first and the deploy it on BCS
6. [Processes - Execute the app as one or more stateless processes](https://12factor.net/processes)   
    Service is stateless with DRF, receives request and then sends response, all data a response needs comes from database or request
7. [Port binding - Export services via port binding](https://12factor.net/port-binding)   
    Binding a port is necessary to run service
8. [Concurrency - Scale out via the process model](https://12factor.net/concurrency)    
    Using Gunicorn for HTTP request and Celery for backend service, both of them support concurrency
9. [Disposability - Maximize robustness with fast startup and graceful shutdown](https://12factor.net/disposability)    
    Services start and shutdown fast, and when deploying on Blueking PaaS, it's undetectable when rollup
10. [Dev/prod parity - Keep development, staging, and production as similar as possible](https://12factor.net/dev-prod-parity)    
    Blueking PaaS provides almost the same running environment for staging and production
11. [Logs - Treat logs as event streams](https://12factor.net/logs)      
    All logs is collected to BkLog while using Blueking PaaS
12. [Admin processes - Run admin/management tasks as one-off processes](https://12factor.net/admin-processes)   
    Django's manage commands are all running as one-off processes, run and then exit
