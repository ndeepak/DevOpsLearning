### DAY 1: Java Build and Deployment End-To-End Workflow

#### #1 Java Build and Deployment End-To-End Workflow

**Overview:**

The Java build and deployment workflow encompasses the complete process from writing code to deploying a Java application. This workflow includes:

1. **Code Compilation**: Translating Java source code into bytecode using the Java Compiler (javac).
2. **Packaging**: Bundling compiled code, dependencies, and resources into deployable units such as JAR (Java ARchive) or WAR (Web Application ARchive) files.
3. **Testing**: Running automated tests to ensure code quality and functionality.
4. **Deployment**: Installing the packaged application onto a server or application container for execution.
5. **Continuous Integration/Continuous Deployment (CI/CD)**: Automating the build, test, and deployment processes to ensure consistent and reliable delivery.

#### #2 Basics

**Introduction to Java Programming and Manual Compilation:**

Java is a versatile and powerful programming language widely used for building web applications, enterprise software, and mobile applications. Understanding the basics of Java programming and the manual compilation process is crucial for any developer.
**Manual Compilation Example:**
1. **Write a Java Program**:
```
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}

```
	
2. **Compile the Program**:   
    `$ javac HelloWorld.java`
    This generates a `HelloWorld.class` file containing the bytecode.
    
3. **Run the Program**:
    `$ java HelloWorld`
    Output: `Hello, World!`
    
#### #3 What is Maven? Why Do We Need a Build Tool?
**Maven Explanation:**
Maven is a build automation tool used primarily for Java projects. It simplifies the build process, manages dependencies, and provides a standardized way to build, test, and deploy applications.
**Why Maven?**
- **Dependency Management**: Automatically downloads and includes required libraries and dependencies.
- **Standardization**: Provides a consistent structure for projects, making it easier to understand and maintain.
- **Build Lifecycle**: Automates repetitive tasks such as compilation, packaging, and deployment.
- **Plugins**: Extensible through plugins for various tasks, including testing, reporting, and code analysis.

#### #4 Installation
**Steps to Install JDK and Maven on Unix-based Systems:**
**JDK Installation**:
1. **Update Package List**:
    `$ sudo apt-get update`
    
2. **Install JDK**:
    `$ sudo apt-get install openjdk-8-jdk`
    

**Maven Installation**:
1. **Update Package List**:
    `$ sudo apt-get update`
    
2. **Install Maven**:
    `$ sudo apt-get install maven`
    

**Verify Installations**:
1. **Check Java Version**:
    `$ java -version`
2. **Check Maven Version**:
    `$ mvn -version`
3. **Verify Java Installation Path**:
    `$ which java`
    
4. **Verify Maven Installation Path**:    
    `$ which mvn`
    

#### #5 Test Your Knowledge
**Test Your Understanding of Build and Deployment Workflows**:
**Questions**:
1. What are the steps involved in the Java build and deployment workflow?
2. How do you manually compile and run a Java program?
3. What is the role of Maven in Java development?
4. Why is dependency management important in a Java project?
5. How do you verify the installation of JDK and Maven on a Unix-based system?

**Answers**:
1. Steps include code compilation, packaging, testing, deployment, and CI/CD automation.
2. Write a Java program, compile it using `javac`, and run it using `java`.
3. Maven simplifies the build process, manages dependencies, and provides a standardized build lifecycle.
4. Dependency management ensures that all required libraries are included and up-to-date, reducing conflicts and issues.
5. Use the commands `java -version`, `mvn -version`, `which java`, and `which mvn` to verify installations.

**Interactive Exercise**:
**Write, Compile, and Run a Java Program**:
1. Create a file `Test.java` with the following content:
```
public class Test {
    public static void main(String[] args) {
        System.out.println("Java Build and Deployment Workflow!");
    }
}
```
2. Compile the program:
    `$ javac Test.java`
    
3. Run the program:
    `$ java Test`
    
4. Verify Maven installation:
    `$ mvn -version`
    
**Summary**: Understanding the Java build and deployment workflow, along with the basics of Java programming and Maven, is essential for developers. This knowledge ensures efficient and standardized project management, making the development process smoother and more reliable.

---
### DAY 2: Maven's Standard Project Layout

#### #6 Maven's Standard Project Layout
**Description:**
Maven enforces a standard project layout to organize source code, test code, and resources, making it easier for developers to navigate and understand the structure of a project. The standard layout includes directories for main source code, test source code, and resources, along with a `pom.xml` file that manages project configurations and dependencies.
##### Example Project Structure
```
project
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── ProjectApp.java
    └── test
        └── java
            └── com
                └── example
                    └── ProjectAppTest.java

```
**Explanation:**
- `pom.xml`: The Project Object Model file that contains project configuration, dependencies, and build instructions.
- `src/main/java`: Directory for main Java source files.
- `src/test/java`: Directory for test Java source files.
##### Sample Java Application
**ProjectApp.java:**
```
package com.example;

public class ProjectApp {
    public static void main(String[] args) {
        System.out.println("Hello, Maven Project!");
    }
}
```
**ProjectAppTest.java:**
```
package com.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class ProjectAppTest {
    @Test
    public void testApp() {
        assertEquals("Hello, Maven Project!", "Hello, Maven Project!");
    }
}
```
#### #7 Building the Maven Project

**Instructions to Install Git, Clone a Project, and Build it Using Maven:**
##### Install Git
```
$ sudo apt-get update
$ sudo apt-get install git
$ git --version  # Verify installation
```

##### Clone a Project
`$ git clone https://github.com/username/project.git`

##### Build the Project with Maven
`$ cd project $ mvn install`

**Maven Build Lifecycle Phases:**
1. **initialize:** Prepares the project with initial prerequisites (e.g., creates necessary directory structure).
2. **validate:** Validates the project's folder structure.
3. **compile:** Compiles the main Java code.
4. **testCompile:** Compiles the test Java code.
5. **test:** Runs the test cases and generates test reports.
6. **package:** Creates JAR/WAR.
7. **install:** Copies built artifacts (JAR/WAR) into the local repository (`$USER_HOME/.m2`).

#### #8 Understanding `pom.xml` File Structure
**Explanation of `pom.xml` File:**
The `pom.xml` file is the core of a Maven project. It configures the build settings, dependencies, and plugins. Here’s a basic structure:

##### Example `pom.xml` Structure
```
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>project</artifactId>
    <version>1.0-SNAPSHOT</version>
    
    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```
**Key Elements:**

- `<groupId>`: Unique identifier for the project group.
- `<artifactId>`: Unique identifier for the project within the group.
- `<version>`: Version of the project.
- `<properties>`: Configurations such as Java version.
- `<dependencies>`: Libraries required for the project.

#### #9 Artifact Path in Local Repository `.m2`
**Details on Local Repository:**
Maven stores downloaded dependencies and built artifacts in the local repository located at `$USER_HOME/.m2/repository`.
##### Example Artifact Path

`$USER_HOME/.m2/repository/com/example/project/1.0-SNAPSHOT/project-1.0-SNAPSHOT.jar`

**Explanation:**

- **`$USER_HOME/.m2/repository`**: Root directory for the local repository.
- **`com/example/project`**: Group and artifact ID directory structure.
- **`1.0-SNAPSHOT`**: Version directory.
- **`project-1.0-SNAPSHOT.jar`**: Built artifact.

---
### Example Maven Project Walkthrough
**Create a Maven Project:**
1. **Generate a Project Directory Structure:**
`$ mvn archetype:generate -DgroupId=com.example -DartifactId=project -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false`

2. **Navigate to the Project Directory:**
`$ cd project`

3. **Examine the Directory Structure:**
`$ tree`

4. **Edit `src/main/java/com/example/App.java`:**
```
package com.example;

public class App {
    public static void main(String[] args) {
        System.out.println("Hello, Maven Project!");
    }
}

```
5. **Edit `src/test/java/com/example/AppTest.java`:**
```
package com.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {
    @Test
    public void testApp() {
        assertEquals("Hello, Maven Project!", "Hello, Maven Project!");
    }
}
```

6. **Build the Project:**
`$ mvn install`

7. **Run the Application:**
`$ java -cp target/project-1.0-SNAPSHOT.jar com.example.App`

Output: `Hello, Maven Project!`

**Verify the Local Repository:**
`$ ls $USER_HOME/.m2/repository/com/example/project/1.0-SNAPSHOT/`

This comprehensive guide covers the fundamental aspects of Maven's standard project layout, building a Maven project, understanding the `pom.xml` file, and managing the local repository.

---
## DAY 3: WEB Application Build and Deployment

### PROJECT-02: WEB Application Build and Deployment
Building and deploying a web application using Maven involves several steps, from setting up the development environment to deploying the application on a Tomcat server. This guide provides a comprehensive walkthrough of the process.
#### Build and Deploy a Web Application
1. **Install Git:**
`$ sudo apt-get update $ sudo apt-get install git $ git --version  # Verify installation`

2. **Clone the Project from Git:**
`$ git clone https://github.com/username/project.git`

3. **Build the Project with Maven:**
`$ cd project $ mvn install`

4. **Check the Final Artifact (WAR File):**
`$ ls target`

5. **Set Up Tomcat for Deployment:**
- Download and install Apache Tomcat from the official website.
- Configure the `CATALINA_HOME` and `TOMCAT_HOME` environment variables.

6. **Deploy `project.war` into Tomcat Deployment Path:**
`$ cp target/project.war $TOMCAT_HOME/webapps`

7. **Start Tomcat Server:**
`$ cd $TOMCAT_HOME/bin $ ./startup.sh`

8. **Access the Application via URL:**
Open your web browser and navigate to:
`http://localhost:8080/project`

---
### Project: 3 (Real-time End-to-End Build and Deployment Process)

Building and deploying a larger-scale application involves similar steps as before, with additional steps to deploy the application on a remote Tomcat server.
#### Build and Deploy a Real-time Application
1. **Install Git:**
`$ sudo apt-get update $ sudo apt-get install git`

2. **Clone the 'project' Application from GitHub:**
`$ git clone https://github.com/username/project.git`

3. **Build 'project' Application with Maven:**
`$ cd project $ mvn install`

4. **Deploy `project.war` to Remote Tomcat Server:**
`$ cp target/project.war $TOMCAT_HOME/webapps`

5. **Start Tomcat Server on the Remote Machine:**
- Connect to the remote server via SSH.
`$ ssh user@remote_host $ cd $TOMCAT_HOME/bin $ ./startup.sh`

6. **Access the Deployed Application via URL:**
Open your web browser and navigate to:
`http://remote_host_ip:8080/project`

---
### Example: Complete Process with Detailed Steps
1. **Installing Git and Cloning the Repository:**
`$ sudo apt-get update $ sudo apt-get install git $ git clone https://github.com/username/project.git $ cd project`

2. **Building the Project with Maven:**
`$ mvn clean install`

3. **Deploying the WAR File to Tomcat:**
- Assuming Tomcat is installed and the `TOMCAT_HOME` environment variable is set.
`$ cp target/project.war $TOMCAT_HOME/webapps`

4. **Starting the Tomcat Server:**
`$ cd $TOMCAT_HOME/bin $ ./startup.sh`

5. **Accessing the Application:**
- Open your browser and go to:
`http://localhost:8080/project`

### Additional Tips and Best Practices

- **Environment Variables:** Ensure `JAVA_HOME` and `M2_HOME` (Maven) are correctly set in your environment.
- **Automated Deployment:** Consider using CI/CD tools like Jenkins to automate the build and deployment process.
- **Remote Deployment:** For remote deployments, SCP or FTP can be used to transfer the WAR file to the server.
- **Logging and Monitoring:** Set up logging and monitoring tools to keep track of application performance and issues.

By following these detailed steps and tips, you can streamline your Java web application build and deployment process, ensuring a smooth and efficient workflow from development to production.

---