### Setting Up GitLab in Ubuntu Using Docker
This guide will walk you through setting up GitLab on an Ubuntu server using Docker. We'll use Docker Compose to manage the GitLab and GitLab Runner containers.
#### Prerequisites
- Ubuntu server
- Docker installed
- Docker Compose installed
#### Step 1: Install Docker and Docker Compose
1. **Update the package index:**
    `sudo apt-get update`
    
2. **Install Docker:**
    `sudo apt-get install -y docker.io`
    
3. **Install Docker Compose:**
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```    
4. **Verify the installation:**
```
    docker --version 
    docker-compose --version
```
#### Step 2: Create Docker Compose Configuration
1. **Create a directory for GitLab:**
    `mkdir ~/gitlab cd ~/gitlab`
    
2. **Create `docker-compose.yml` file:**
```
version: '3.6'

services:
  gitlab:
    container_name: gitlab-web
    image: 'gitlab/gitlab-ce:15.9.8-ce.0'
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://ndeepak.gitlab.com'
        # Add any other gitlab.rb configuration here, each on its own line
    ports:
      - '80:80'
      - '443:443'
      - '222:22'
      - '5050:5050'
    volumes:
      - '$GITLAB_HOME/config:/etc/gitlab'
      - '$GITLAB_HOME/logs:/var/log/gitlab'
      - '$GITLAB_HOME/data:/var/opt/gitlab'
    shm_size: '256m'

  dind:
    container_name: docker-in-docker
    image: docker:20-dind
    restart: always
    privileged: true
    environment:
      DOCKER_TLS_CERTDIR: ""
    command:
      - --storage-driver=overlay2
    volumes:
      - './data/dind/docker:/var/lib/docker'

  runner:
    container_name: gitlab-runner
    image: registry.gitlab.com/gitlab-org/gitlab-runner:alpine
    restart: always
    volumes:
      - './config:/etc/gitlab-runner:z'
      - './data/runner/cache:/cache'
    environment:
      - DOCKER_HOST=tcp://docker-in-docker:2375

```
3. **Create environment variable file:**
    `export GITLAB_HOME=$HOME/gitlab`
#### Step 3: Launch GitLab with Docker Compose
1. **Start the services:**
    `docker-compose up -d`
    
2. **Check the status of the containers:**
    `docker-compose ps`
    
3. **Access GitLab:**
    Open a web browser and go to `http://your_server_ip` or `http://ndeepak.gitlab.com`.
#### Step 4: Configure GitLab Runner
1. **Register the GitLab Runner:**
    `docker exec -it gitlab-runner gitlab-runner register`
    
    - Enter the GitLab instance URL: `http://ndeepak.gitlab.com/`
    - Enter the registration token from GitLab
    - Enter a description for the runner
    - Enter the tags for the runner (e.g., docker)
    - Choose the executor: `docker`
    - Enter the default Docker image: `alpine:latest`
2. **Verify the Runner registration:**
    Go to your GitLab instance -> Admin Area -> Overview -> Runners to check if the runner is registered.
#### Step 5: Example `.gitlab-ci.yml` Configuration
Create a `.gitlab-ci.yml` file in your repository to define the CI/CD pipeline.
```
image: python:3.9

services:
  - docker:dind

stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2

before_script:
  - docker info

build:
  stage: build
  script:
    - docker build -t my-image:latest .

test:
  stage: test
  script:
    - docker run --rm my-image:latest

deploy:
  stage: deploy
  script:
    - echo "Deploy step (if needed)"
```
### Summary
- **Docker Installation:** Installed Docker and Docker Compose on Ubuntu.
- **Docker Compose Configuration:** Created a `docker-compose.yml` file to set up GitLab and GitLab Runner containers.
- **Launch GitLab:** Started GitLab services with Docker Compose.
- **Configure Runner:** Registered a GitLab Runner and created an example CI/CD pipeline.

By following these steps, you can set up a GitLab instance with GitLab Runner using Docker on an Ubuntu server. This setup enables you to manage your Git repositories and automate your CI/CD pipelines efficiently.