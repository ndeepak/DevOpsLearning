### `GIT_STRATEGY` in GitLab CI/CD
#### What is `GIT_STRATEGY`?
`GIT_STRATEGY` is a predefined variable in GitLab CI/CD that determines how GitLab Runner fetches the repository for each job. The possible values for `GIT_STRATEGY` are:
- **clone**: Clones the repository from scratch.
- **fetch**: Fetches changes from the repository.
- **none**: Does not fetch the repository.

#### Default Value
The default value for `GIT_STRATEGY` is `fetch`.
#### Use Cases
1. **clone**
    - **Scenario**: You want to ensure a completely clean working directory for your job.
    - **Use Case**: When dealing with complex dependency issues, ensuring no residual files or changes affect the job. Useful in jobs where the repository's state should be pristine.
    - **Example**:        
```
variables:
  GIT_STRATEGY: clone
```
        
2. **fetch**
    - **Scenario**: You want to update the repository by fetching only the latest changes.
    - **Use Case**: Faster than cloning since it only downloads changes. Ideal for most CI jobs where the previous state does not negatively impact the job.
    - **Example**:
```
variables:
  GIT_STRATEGY: fetch
```
        
3. **none**
    - **Scenario**: You want to skip fetching the repository.
    - **Use Case**: Jobs that do not require the repository's code, such as deployment jobs where artifacts from previous jobs are used. Also useful for maintenance jobs or jobs that only require a small script.
    - **Example**:
```
variables:
  GIT_STRATEGY: none
```
        
#### Setting `GIT_STRATEGY` in `.gitlab-ci.yml`
You can set the `GIT_STRATEGY` variable in the `.gitlab-ci.yml` file at the global level or per job.
- **Global Level**:
```
variables:
  GIT_STRATEGY: clone
```
    
- **Per Job Level**:
```
build:
  stage: build
  variables:
    GIT_STRATEGY: fetch
  script:
    - echo "Building the project"
```
    

#### Benefits and Drawbacks
- **clone**
    - **Benefits**: Ensures a clean working directory.
    - **Drawbacks**: Slower due to downloading the entire repository.
- **fetch**
    - **Benefits**: Faster than cloning, reduces the amount of data transferred.
    - **Drawbacks**: May not be suitable if the repository's state is critical.
- **none**
    - **Benefits**: Fastest, minimal data transfer.
    - **Drawbacks**: Only suitable for jobs that do not require the repository.

#### Practical Examples
1. **Ensuring Clean State for Tests**:
```
test:
  stage: test
  variables:
    GIT_STRATEGY: clone
  script:
    - echo "Running tests"
```
    
2. **Optimizing for Speed in Deployment**:
```
deploy:
  stage: deploy
  variables:
    GIT_STRATEGY: none
  script:
    - echo "Deploying application"
```
    
3. **Regular Build Job**:
```
build:
  stage: build
  variables:
    GIT_STRATEGY: fetch
  script:
    - echo "Building the application"
```
By using `GIT_STRATEGY` appropriately, you can optimize your CI/CD pipeline's efficiency, speed, and reliability.