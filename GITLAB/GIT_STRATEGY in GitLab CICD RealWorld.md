### `GIT_STRATEGY` in GitLab CI/CD: A Real-World Example

#### Scenario
You are developing a Java project with a GitLab CI/CD pipeline that includes stages for building, testing, and deploying the application. The build stage requires a clean clone of the repository, the test stage can use fetch for faster execution, and the deploy stage doesn't require the repository at all since it uses artifacts from the build stage.
#### Project Structure
- Project name: `JavaApp`
- GitLab CI/CD stages: `build`, `test`, `deploy`
- Build tool: Maven
- Deployment: Using a script to deploy to a server

#### `.gitlab-ci.yml` Configuration
```
image: maven:3.8.1-jdk-11

stages:
  - build
  - test
  - deploy

# Global variable for default strategy
variables:
  GIT_STRATEGY: fetch

before_script:
  - echo "Starting CI pipeline for JavaApp"
  - echo "Current GIT_STRATEGY: $GIT_STRATEGY"

build_project:
  stage: build
  variables:
    GIT_STRATEGY: clone  # Ensuring a clean state
  script:
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 week

test_project:
  stage: test
  script:
    - mvn test

deploy_project:
  stage: deploy
  variables:
    GIT_STRATEGY: none  # No need to fetch the repo
  script:
    - echo "Deploying to server..."
    - scp target/*.jar user@server:/path/to/deploy
```

#### Explanation
1. **Global Variables**:
```
variables:
  GIT_STRATEGY: fetch
```    
    This sets the default `GIT_STRATEGY` to `fetch` for all jobs. The `fetch` strategy downloads only the latest changes, which speeds up the pipeline.
    
2. **Build Stage**:
```
build_project:
  stage: build
  variables:
    GIT_STRATEGY: clone
  script:
    - mvn clean package
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 week
```
    In the build stage, we override the `GIT_STRATEGY` to `clone` to ensure a clean working directory. This is important for a clean build environment. The build artifact (a JAR file) is stored and will be used in subsequent stages.
    
3. **Test Stage**:
```
test_project:
  stage: test
  script:
    - mvn test
```    
    The test stage uses the default `fetch` strategy to get the latest changes. This is typically faster and sufficient for running tests since a completely clean state isn't required.
    
4. **Deploy Stage**:
```
deploy_project:
  stage: deploy
  variables:
    GIT_STRATEGY: none
  script:
    - echo "Deploying to server..."
    - scp target/*.jar user@server:/path/to/deploy
```
    
    In the deploy stage, the `GIT_STRATEGY` is set to `none` because the deployment process only uses the artifact generated in the build stage. This minimizes unnecessary fetching and speeds up the deployment process.
    
#### Running the Pipeline
When you commit your `.gitlab-ci.yml` file to your repository, GitLab will automatically start the pipeline:
1. **Build Stage**:
    - Clones the repository.
    - Runs `mvn clean package`.
    - Stores the JAR file as an artifact.
2. **Test Stage**:
    - Fetches the latest changes.
    - Runs `mvn test`.
3. **Deploy Stage**:
    - Does not fetch the repository.
    - Uses the stored JAR file and deploys it to the server.

This setup optimizes each stage of the CI/CD pipeline by using the appropriate `GIT_STRATEGY`, ensuring clean builds, fast tests, and efficient deployments.