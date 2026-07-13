# 1. What is OpenJDK?

**OpenJDK (Open Java Development Kit)** is the open-source reference implementation of the Java Platform.

It contains:

- Java compiler (`javac`)
- Java runtime (`java`)
- Core Java libraries
- JVM (Java Virtual Machine)
- Development tools

When you write:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

OpenJDK provides:

```java
javac Hello.java
java Hello
```

to compile and execute the code.

---

# 2. What is Eclipse Temurin?

Temurin is a distribution of OpenJDK maintained by the Eclipse Adoptium project.

Think of it this way:

```java
Java Specification
        |
        v
     OpenJDK
        |
   --------------------
   |        |         |
 Temurin Corretto Zulu
   |        |         |
Adoptium   AWS      Azul
```

Different vendors package OpenJDK and provide binaries.

Examples:

|Vendor|Distribution|
|---|---|
|Eclipse Adoptium|Temurin|
|AWS|Corretto|
|Azul|Zulu|
|Oracle|Oracle JDK|

Temurin is:
- Free
- Open Source
- TCK certified
- Enterprise ready
- Widely used in production

---

# 3. Understanding Version 17.0.12+7

The version:

```
17.0.12+7
```

means:

### Major Version

```
17
```

Java 17

Java 17 is an LTS (Long Term Support) release.

Common LTS versions:

```
Java 8
Java 11
Java 17
Java 21
```

---

### Security/Patch Version

```
0.12
```

means:

```
17.0.12
```

Twelve patch releases after Java 17.

Contains:

- Security fixes
- Bug fixes
- Performance improvements

No breaking API changes.

---

### Build Number

```
+7
```

means:

```
Build 7
```

of the 17.0.12 release.

Think of it as:

```
Java 17
Patch level 12
Build number 7
```

---

# 4. What Does "Developer Package" Mean?

You may see:

```
OpenJDK Temurin 17.0.12+7
```

or

```
OpenJDK Temurin 17.0.12+7 (Developer Package)
```

The developer package means you installed the **JDK**, not just the runtime.

Contains:

|Tool|Purpose|
|---|---|
|java|Run applications|
|javac|Compile code|
|jar|Create JAR files|
|javadoc|Generate documentation|
|jdb|Java debugger|
|jdeps|Dependency analysis|
|jlink|Create custom runtimes|
|jshell|Interactive Java shell|
|jpackage|Package applications|

---

# 5. JDK vs JRE

Many beginners confuse these.

## JRE

Java Runtime Environment

Contains:

```
java
JVM
Libraries
```

Can run programs.

Cannot compile.

---

## JDK

Java Development Kit

Contains:

```
JRE
javac
javadoc
jar
debuggers
development tools
```

Can:

- Run applications
- Compile applications
- Build applications

Diagram:

```
JDK
 |
 +-- JRE
      |
      +-- JVM
```

---

# 6. Verify Installation

Check version:

```
java -version
```

Output:

```java
openjdk version "17.0.12" 2024-07-16
OpenJDK Runtime Environment Temurin-17.0.12+7
OpenJDK 64-Bit Server VM Temurin-17.0.12+7
```

Check compiler:

```
javac -version
```

Output:

```
javac 17.0.12
```

---

# 7. Important Directories

On Linux:

```
/usr/lib/jvm/
```

Example:

```
/usr/lib/jvm/temurin-17-jdk
```

Contents:

```
bin/
lib/
conf/
include/
jmods/
```

---

### bin/

Contains executables:

```
java
javac
jar
jcmd
jstack
jmap
jstat
```

---

### lib/

Java libraries and JVM files.

---

### include/

Used when writing JNI code.

Example:

```
JNIEXPORT void JNICALL
Java_Test_print(JNIEnv *env, jobject obj)
{
}
```

---

### jmods/

Contains Java modules.

Example:

```
java.base.jmod
java.sql.jmod
java.xml.jmod
```

Used by `jlink`.

---

# 8. Java Modules in JDK 17

Since Java 9, Java uses the Module System.

Example:

```
module myapp {
    requires java.sql;
}
```

Module examples:

```
java.base
java.sql
java.xml
java.logging
java.net.http
```

View modules:

```
java --list-modules
```

---

# 9. Useful Developer Tools

## javac

Compile Java source

```
javac Main.java
```

Creates:

```
Main.class
```

---

## jar

Package classes

```
jar cf app.jar *.class
```

---

## javadoc

Generate HTML docs

```
javadoc MyClass.java
```

---

## jshell

Interactive Java shell

```
jshell
```

Example:

```
jshell> 10 + 20
30
```

---

## jdeps

Dependency analyzer

```
jdeps app.jar
```

Shows:

```
java.base
java.sql
```

dependencies.

---

## jlink

Create minimal runtime.

Example:

```bash
jlink \
--module-path $JAVA_HOME/jmods \
--add-modules java.base \
--output custom-runtime
```

Instead of shipping a 300+ MB JDK, you can ship a tiny runtime.

---

# 10. JVM Inside Temurin

The JVM executes bytecode.

Flow:

```scss
Java Source
      |
      v
   javac
      |
      v
 Bytecode (.class)
      |
      v
    JVM
      |
      v
 Native Machine Code
```

---

# 11. Important JVM Components

## Class Loader

Loads classes.

```
Main.class
String.class
ArrayList.class
```

---

## Bytecode Verifier

Checks:

```
Type safety
Memory safety
Access rules
```

---

## JIT Compiler

Just-In-Time compiler.

Converts:

```
Bytecode
```

into

```
Native machine code
```

for better performance.

---

## Garbage Collector

Automatically frees memory.

Example:

```
obj = null;
```

Unused objects are eventually reclaimed.

---

# 12. Useful JVM Diagnostic Commands

### View running JVMs

```
jps
```

Example:

```
12345 MyApplication
```

---

### Thread dump

```
jstack 12345
```

Useful when debugging hangs.

---

### Heap dump

```
jmap -dump:live,file=heap.hprof 12345
```

Used for memory leak analysis.

---

### JVM statistics

```
jstat -gc 12345
```

Shows GC activity.

---

### JVM command utility

```
jcmd 12345 VM.flags
```

Shows JVM flags.

---

# 13. Why Enterprises Use Temurin

Common reasons:

1. Free and open source
2. Long-term support
3. Stable updates
4. TCK certified
5. Production-ready builds
6. Available on Linux, Windows, macOS, Docker, Kubernetes environments

---

# 14. Real-World Use Cases

Temurin 17 is commonly used to run:

- Spring Boot applications
- Apache Tomcat
- Jenkins
- Kafka clients
- Hadoop ecosystem tools
- Enterprise banking applications
- Microservices running in containers

Example:

```
java -jar myapp.jar
```

or

```
java \
-Xms2G \
-Xmx4G \
-jar myapp.jar
```

---

# 15. If You Are a Linux/System Engineer

You should be comfortable with:

```bash
java -version
javac -version
jps
jcmd
jstack
jmap
jstat
jar
jdeps
jlink
```

and understand:

```bash
JDK vs JRE
JVM Architecture
Garbage Collection
Class Loading
Java Modules
Heap vs Stack
JIT Compilation
Thread Dumps
Heap Dumps
```

These are the concepts you'll frequently encounter when administering Java-based applications such as Spring Boot services, Jenkins, SonarQube, Kafka tools, or enterprise banking software running on Linux servers.