# BPM GitLab CI/CD Pipeline with Apache Ant
## Introduction
This guide covers setting up a CI/CD pipeline using GitLab CI and Apache Ant. We will:
1. Configure a `.gitlab-ci.yml` file.
2. Set up an Apache Ant build process.
3. Document the pipeline configuration and build process.

## Prerequisites
- GitLab account and a GitLab repository.
- Basic understanding of Git and CI/CD concepts.
- Apache Ant installed locally for testing.

## Project Structure
```
bpm-ci/
├── build.xml
├── .gitlab-ci.yml
├── README.md
├── lib/
├── src/
└── dist/
```

- **build.xml**: Apache Ant build script.
- **.gitlab-ci.yml**: GitLab CI/CD pipeline configuration.
- **README.md**: Project documentation.
- **lib/**: Directory for library dependencies.
- **src/**: Directory for source code.
- **dist/**: Directory for build outputs (e.g., JAR files).

## Step-by-Step Guide

### 1. Create Apache Ant Build Script (`build.xml`)
```
as per your need
```

### 2. Configure GitLab CI/CD Pipeline (`.gitlab-ci.yml`)

Create a `.gitlab-ci.yml` file in the root directory of your project:
```
image: frekele/ant

stages:
  - build

variables:
  GIT_STRATEGY: clone

before_script:
  # Ensure Ant is installed
  - apt-get update && apt-get install -y ant

build_project:
  stage: build
  script:
    - ls -la
    - ant compile
    - ant jar
  artifacts:
    paths:
      - dist/*.jar
    expire_in: 1 week
```

### Pipeline Breakdown

- **image**: Specifies the Docker image to use for the CI/CD pipeline. Here, we use `frekele/ant`, which has Apache Ant pre-installed.
- **stages**: Defines the stages of the pipeline. In this case, we have a single stage: `build`.
- **variables**: Defines variables used in the pipeline. `GIT_STRATEGY: clone` ensures the repository is fully cloned instead of being fetched.
- **before_script**: Commands to be run before the main script. Here, we update the package list and install Apache Ant.
- **build_project**: Defines the build job.
    - **stage**: Specifies the stage this job belongs to (`build`).
    - **script**: The commands to run in this job. We list the contents of the directory, compile the project, and create a JAR file using Ant.
    - **artifacts**: Specifies which files to save as artifacts. In this case, we save any JAR files in the `dist` directory and set them to expire in 1 week.

### Running the Pipeline

When changes are pushed to the repository, GitLab CI/CD will automatically run the pipeline defined in the `.gitlab-ci.yml` file. The pipeline will:

1. Use the `frekele/ant` Docker image.
2. Clone the repository.
3. Update the package list and install Apache Ant.
4. List the directory contents.
5. Compile the project using Ant.
6. Create a JAR file using Ant.
7. Save the JAR file as an artifact.

### Viewing Artifacts

After the pipeline runs successfully, you can download the generated JAR file from the GitLab CI/CD job page.

### Build and Deployment

- **Compile**: Runs the `ant compile` command to compile the source code.
- **Jar**: Runs the `ant jar` command to create a JAR file from the compiled code.

## Project Structure

- **build.xml**: Ant build script.
- **src/**: Source code directory.
- **lib/**: Library directory.
- **dist/**: Directory where the JAR file will be placed after the build.

## Commands

- `ant compile`: Compiles the source code.
- `ant jar`: Creates a JAR file from the compiled code.

## Requirements

- Apache Ant
- GitLab CI/CD

## Setting Up Locally

1. Install Apache Ant.
2. Clone the repository.
3. Run `ant compile` to compile the source code.
4. Run `ant jar` to create the JAR file.
5. Find the JAR file in the `dist` directory.

## Conclusion

This project demonstrates a simple CI/CD pipeline using Apache Ant and GitLab CI. The pipeline compiles the source code and creates a JAR file, which is then saved as an artifact.
```
### 4. Push Your Changes to GitLab

Push your project files, including `.gitlab-ci.yml`, `build.xml`, and `README.md`, to your GitLab repository:

```bash
git add .
git commit -m "Add GitLab CI/CD pipeline and Ant build configuration"
git push origin main
```
### 5. Verify Pipeline Execution

1. Go to your GitLab repository.
2. Navigate to the **CI/CD** > **Pipelines** section.
3. Verify that the pipeline is triggered and running.
4. Check the pipeline logs to ensure the build is successful.
5. Download the artifacts (JAR file) from the pipeline job page.

### Summary

You have now successfully set up a CI/CD pipeline using GitLab CI and Apache Ant. The pipeline automates the process of compiling the source code and creating a JAR file, which is then saved as an artifact for easy access.