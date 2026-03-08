## Maven Lifecycle (Detailed Explanation)

### Definition

A **Maven Lifecycle** is a **sequence of phases used to build and manage a project**.
Each phase performs a specific task like **compiling code, running tests, packaging artifacts, and deploying them**.

When you run a command like:

```bash
mvn package
```

Maven **executes that phase and all phases before it in the lifecycle**.

---

# 1. Maven Has 3 Lifecycles

| Lifecycle             | Purpose                            |
| --------------------- | ---------------------------------- |
| **Clean Lifecycle**   | Removes previous build artifacts   |
| **Default Lifecycle** | Builds and deploys the application |
| **Site Lifecycle**    | Generates project documentation    |

---

# 2. Clean Lifecycle

### Purpose

Removes previously generated build files.

### Phases

| Phase      | Description                |
| ---------- | -------------------------- |
| pre-clean  | Tasks before cleaning      |
| clean      | Deletes `target` directory |
| post-clean | Tasks after cleaning       |

### Example Command

```bash
mvn clean
```

### What Happens

Maven executes:

```
maven-clean-plugin:clean
```

### Output Location

Before running:

```
project
 ├── src
 └── target
```

After running:

```
target directory deleted
```

---

# 3. Default Lifecycle (Main Build Lifecycle)

This lifecycle contains **23 phases**, but commonly used phases are below.

---

## Phase 1: Validate

### Purpose

Validates project structure and checks `pom.xml`.

### Example Command

```bash
mvn validate
```

### What Happens

* Maven checks if project structure is correct.

### Output

No files generated.

---

## Phase 2: Compile

### Purpose

Compiles source code.

### Example Command

```bash
mvn compile
```

### What Happens

Plugin used:

```
maven-compiler-plugin
```

### Source Code Location

```
src/main/java
```

### Output Location

```
target/classes
```

Example:

```
src/main/java/com/app/UserService.java
```

Output:

```
target/classes/com/app/UserService.class
```

---

## Phase 3: Test

### Purpose

Runs unit tests.

### Example Command

```bash
mvn test
```

### Plugin Used

```
maven-surefire-plugin
```

### Test Code Location

```
src/test/java
```

Example test file:

```
UserServiceTest.java
```

### Output Locations

Compiled tests:

```
target/test-classes
```

Test reports:

```
target/surefire-reports
```

Example files:

```
TEST-UserServiceTest.xml
UserServiceTest.txt
```

---

## Phase 4: Package

### Purpose

Creates final artifact (JAR or WAR).

### Example Command

```bash
mvn package
```

### Plugins Used

```
maven-jar-plugin
```

or

```
maven-war-plugin
```

### Output Location

```
target/
```

Example:

```
target/myapp-1.0.jar
```

---

## Phase 5: Verify

### Purpose

Runs additional checks (integration tests).

### Example Command

```bash
mvn verify
```

Plugin used:

```
maven-failsafe-plugin
```

---

## Phase 6: Install

### Purpose

Installs artifact into **local Maven repository**.

### Example Command

```bash
mvn install
```

### Output Location

```
~/.m2/repository
```

Example:

```
~/.m2/repository/com/app/myapp/1.0/myapp-1.0.jar
```

Used by other local projects.

---

## Phase 7: Deploy

### Purpose

Uploads artifact to **remote repository**.

Example tools:

* Nexus
* Artifactory

### Command

```bash
mvn deploy
```

### Output

Artifact uploaded to remote repo.

Example:

```
http://nexus.company.com/repository/maven-releases
```

---

# 4. Full Default Lifecycle Flow

When you run:

```bash
mvn clean install
```

Execution flow:

```
clean
validate
compile
test
package
verify
install
```

---

# 5. Complete Project Example

Project structure:

```
my-app
 ├── pom.xml
 └── src
      ├── main
      │    └── java
      │         └── App.java
      └── test
           └── java
                └── AppTest.java
```

Command:

```bash
mvn clean package
```

Execution result:

```
target/
 ├── classes
 │    └── App.class
 ├── test-classes
 │    └── AppTest.class
 ├── surefire-reports
 │    └── TEST-AppTest.xml
 └── my-app-1.0.jar
```

---

# 6. Important Maven Concept

### Running a Later Phase Executes Previous Phases

Example:

```bash
mvn package
```

Internally runs:

```
validate
compile
test
package
```

You don't need to run them separately.

---

# 7. Visual Flow

```
Clean Lifecycle
   │
   ▼
clean

Default Lifecycle
   │
   ▼
validate
compile
test
package
verify
install
deploy
```

---

# 8. Interview Style Answer

**Question:** Explain Maven lifecycle.

**Answer:**

Maven lifecycle is a sequence of phases used to build and manage a project. Maven has three lifecycles: **Clean, Default, and Site**.

The **Default lifecycle** handles the main build process with phases like **validate, compile, test, package, install, and deploy**.

For example, when we run `mvn package`, Maven compiles the code, runs unit tests, and generates the final artifact such as a **JAR or WAR file in the target directory**.

---

✅ **Very Common DevOps Interview Follow-up**

**Q:** What is the difference between `mvn package`, `mvn install`, and `mvn deploy`?

| Command   | Result                              |
| --------- | ----------------------------------- |
| `package` | Creates artifact in `target`        |
| `install` | Copies artifact to `.m2 repository` |
| `deploy`  | Uploads artifact to remote repo     |

---

If you want, I can also explain **Maven architecture (Super POM, Effective POM, Plugins, Lifecycle, Repositories)** — this is **one of the most asked DevOps interview topics**.

##################################################################################################################
Since you're preparing **DevOps / Infrastructure Engineer interviews**, understanding **Maven Architecture** clearly helps explain **how Maven actually builds a project**.

---

# Maven Architecture

### Definition

**Maven Architecture** explains how Maven builds a project using **POM files, plugins, repositories, and lifecycle phases**.

It consists of these major components:

1. **POM (Project Object Model)**
2. **Maven Lifecycle**
3. **Plugins**
4. **Repositories**
5. **Dependencies**
6. **Super POM**
7. **Effective POM**

---

# 1. POM (Project Object Model)

### Definition

The **POM file (`pom.xml`)** is the **core configuration file of a Maven project**.
It contains all information needed to build the project.

### Example

```xml
<project>
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.company</groupId>
  <artifactId>payment-service</artifactId>
  <version>1.0</version>

  <dependencies>
     <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.9</version>
     </dependency>
  </dependencies>
</project>
```

### Important Fields

| Field      | Meaning                      |
| ---------- | ---------------------------- |
| groupId    | Organization or company name |
| artifactId | Application name             |
| version    | Version of application       |

Example artifact name generated:

```
payment-service-1.0.jar
```

---

# 2. Maven Lifecycle

The **lifecycle controls the build process**.

Important phases:

```
validate
compile
test
package
verify
install
deploy
```

Example command:

```bash
mvn clean package
```

Result:

```
target/application.jar
```

---

# 3. Maven Plugins

### Definition

Plugins **perform actual tasks during lifecycle phases**.

Maven lifecycle only defines phases — **plugins execute the work**.

### Common Plugins

| Plugin                | Purpose               |
| --------------------- | --------------------- |
| maven-compiler-plugin | Compile Java code     |
| maven-surefire-plugin | Run unit tests        |
| maven-jar-plugin      | Create JAR file       |
| maven-war-plugin      | Create WAR file       |
| maven-clean-plugin    | Clean build directory |

Example:

```
compile phase → maven-compiler-plugin
test phase → maven-surefire-plugin
package phase → maven-jar-plugin
```

---

# 4. Maven Repositories

Repositories store **dependencies and artifacts**.

Three types:

| Repository         | Description                            |
| ------------------ | -------------------------------------- |
| Local Repository   | Developer machine (`~/.m2/repository`) |
| Central Repository | Public repository                      |
| Remote Repository  | Private repo (Nexus, Artifactory)      |

Dependency resolution flow:

```
Local Repo → Remote Repo → Maven Central
```

---

# 5. Dependencies

Dependencies are **external libraries required by the application**.

Example:

```xml
<dependency>
   <groupId>org.springframework</groupId>
   <artifactId>spring-core</artifactId>
   <version>5.3.9</version>
</dependency>
```

Maven downloads dependency to:

```
~/.m2/repository
```

---

# 6. Super POM

### Definition

**Super POM** is the **default POM provided by Maven**.

Every Maven project **inherits from Super POM automatically**.

It contains default configurations like:

* plugin versions
* repository definitions
* build settings

Example repository defined in Super POM:

```
https://repo.maven.apache.org/maven2
```

---

# 7. Effective POM

### Definition

The **Effective POM** is the **final combined configuration** after merging:

```
Project POM + Parent POM + Super POM
```

Command to see it:

```bash
mvn help:effective-pom
```

Example output includes:

* plugins
* dependencies
* repositories
* build configuration

---

# Maven Architecture Flow

```
Developer runs
     │
     ▼
mvn clean package
     │
     ▼
Reads pom.xml
     │
     ▼
Downloads dependencies from repository
     │
     ▼
Executes lifecycle phases
     │
     ▼
Plugins perform tasks
     │
     ▼
Build artifact generated
```

Output:

```
target/myapp.jar
```

---

# Real DevOps Pipeline Example (Jenkins)

In a CI/CD pipeline:

```
Developer pushes code → Git
        │
        ▼
Jenkins pipeline triggered
        │
        ▼
mvn clean package
        │
        ▼
Artifact generated
        │
        ▼
Upload to Nexus
        │
        ▼
Deploy to server
```

---

# Interview Style Answer

**Question:** Explain Maven architecture.

**Answer:**

Maven architecture consists of components such as **POM, lifecycle, plugins, repositories, and dependencies**.
The **POM file (`pom.xml`)** defines project configuration and dependencies. Maven uses **lifecycle phases** like compile, test, and package to build the application. These phases execute tasks through **plugins** such as the compiler plugin or surefire plugin. Dependencies are downloaded from **repositories** like local, central, or remote repositories. Maven also uses a **Super POM** which provides default configurations, and the **Effective POM** which is the final merged configuration used during the build.

---

✅ **Very Common DevOps Cross Questions**

1️⃣ What is the difference between **Super POM and Effective POM**?
2️⃣ What happens internally when we run **`mvn clean install`**?
3️⃣ What is **dependency transitive resolution** in Maven?
4️⃣ What is **dependency scope** in Maven?

---

If you want, I can also explain **Maven Dependency Scopes (`compile`, `provided`, `runtime`, `test`)**, which is **one of the most confusing but frequently asked interview questions**.
