## Maven Repositories

### Definition

A **Maven Repository** is a **storage location where Maven stores and retrieves project dependencies, plugins, and build artifacts** such as **JAR, WAR, and POM files**.

When Maven builds a project, it **downloads required libraries from repositories** and stores them locally for reuse.

---

# 1. Types of Maven Repositories

There are **three main types** of Maven repositories.

## 1️⃣ Local Repository

### Definition

The **Local Repository** is a directory on the **developer's machine** where Maven stores downloaded dependencies.

### Default Location

Linux / Mac:

```bash
~/.m2/repository
```

Windows:

```bash
C:\Users\<username>\.m2\repository
```

### When It Is Used

* When a dependency is downloaded for the **first time**
* When Maven builds a project **offline**
* When Maven checks if dependency already exists locally

### Example

If `spring-core` dependency is used:

```xml
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-core</artifactId>
    <version>5.3.9</version>
</dependency>
```

Maven downloads it to:

```text
~/.m2/repository/org/springframework/spring-core/5.3.9/
```

---

# 2️⃣ Central Repository

### Definition

The **Central Repository** is the **default public repository maintained by the Maven community** where most open-source libraries are stored.

Example:

* Spring
* Hibernate
* Log4j
* Apache libraries

Repository URL:

```
https://repo.maven.apache.org/maven2
```

### When It Is Used

When Maven **cannot find the dependency in the local repository**, it automatically downloads it from the **Central Repository**.

### Example Flow

```text
Developer runs mvn clean package
          │
          ▼
Maven checks Local Repository
          │
     Not found
          │
          ▼
Downloads from Central Repository
          │
          ▼
Stores in Local Repository
```

---

# 3️⃣ Remote Repository (Private Repository)

### Definition

A **Remote Repository** is a **private repository hosted by organizations** to store internal project artifacts.

Common tools used:

* **Nexus Repository Manager**
* **JFrog Artifactory**
* **AWS CodeArtifact**

### When It Is Used

Used in **enterprise environments** to:

* Store **internal libraries**
* Store **company-built artifacts**
* Avoid downloading dependencies directly from the internet

Example:

```
Company builds service-A
        │
        ▼
mvn deploy
        │
        ▼
Artifact uploaded to Nexus
        │
        ▼
Other services can use that artifact
```

Example dependency usage:

```xml
<dependency>
   <groupId>com.company</groupId>
   <artifactId>payment-service</artifactId>
   <version>1.0.0</version>
</dependency>
```

---

# 4. Repository Usage Flow

When Maven builds a project:

```
mvn clean package
       │
       ▼
Check Local Repository
       │
       ▼
If not found
       │
       ▼
Check Remote Repository (Nexus/Artifactory)
       │
       ▼
If not found
       │
       ▼
Check Maven Central
       │
       ▼
Download dependency
       │
       ▼
Store in Local Repository
```

---

# 5. Maven Repository Structure

Example directory structure:

```
repository
 └── org
      └── springframework
           └── spring-core
                └── 5.3.9
                     ├── spring-core-5.3.9.jar
                     ├── spring-core-5.3.9.pom
```

---

# 6. Commands That Use Maven Repositories

### Download Dependencies

```bash
mvn compile
```

### Install artifact to local repo

```bash
mvn install
```

Stores artifact in:

```
~/.m2/repository
```

### Upload artifact to remote repo

```bash
mvn deploy
```

---

# 7. Interview Style Answer

**Question:** What are Maven repositories?

**Answer:**

Maven repositories are **locations where project dependencies, plugins, and build artifacts are stored**. Maven uses three types of repositories:

1. **Local Repository** – Located on the developer machine (`~/.m2/repository`) and stores downloaded dependencies.
2. **Central Repository** – Public repository maintained by Maven that hosts open-source libraries.
3. **Remote Repository** – Private repositories like Nexus or Artifactory used by organizations to store internal artifacts.

During a build, Maven first checks the **local repository**, then **remote repositories**, and finally the **central repository** to download dependencies.

---

✅ **Very Common DevOps Interview Follow-up**

**Q:** What is the difference between `mvn install` and `mvn deploy`?

* **install** → uploads artifact to **local repository**
* **deploy** → uploads artifact to **remote repository (Nexus/Artifactory)**

---