Below is a **complete improved Jenkins Declarative Pipeline** including everything you asked:

* `parameters`
* `triggers`
* `checkout`
* `parallel`
* `retry`
* `when`
* `catchError`
* `manual approval`
* `Docker build & push`
* `Kubernetes deployment`
* `post actions`

After the pipeline, I will **explain every block and command clearly**.

---

# 1. Complete CI/CD Jenkins Pipeline

```groovy
pipeline {

    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'uat', 'prod'], description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run unit tests')
    }

    environment {
        APP_NAME = "payment-service"
        DOCKER_REPO = "nikhilsy/payment-service"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH_NAME}"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/example/payment-service.git'
                    ]]
                ])
            }
        }

        stage('Build Application') {
            steps {
                retry(3) {
                    sh 'mvn clean package'
                }
            }
        }

        stage('Tests and Code Scan') {

            when {
                expression {
                    params.RUN_TESTS == true
                }
            }

            parallel {

                stage('Unit Tests') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh 'mvn test'
                        }
                    }
                }

                stage('SonarQube Scan') {
                    steps {
                        sh 'mvn sonar:sonar'
                    }
                }

            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                """
            }
        }

        stage('Push Docker Image') {

            when {
                anyOf {
                    environment name: 'DEPLOY_ENV', value: 'uat'
                    environment name: 'DEPLOY_ENV', value: 'prod'
                }
            }

            steps {
                sh """
                docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                """
            }
        }

        stage('Approval for Production') {

            when {
                environment name: 'DEPLOY_ENV', value: 'prod'
            }

            steps {
                input message: "Approve deployment to Production?"
            }
        }

        stage('Deploy to Kubernetes') {

            when {
                anyOf {
                    environment name: 'DEPLOY_ENV', value: 'uat'
                    environment name: 'DEPLOY_ENV', value: 'prod'
                }
            }

            steps {
                sh """
                kubectl set image deployment/${APP_NAME} \
                ${APP_NAME}=${DOCKER_REPO}:${BUILD_NUMBER}
                """
            }
        }

    }

    post {

        always {
            echo "Pipeline execution finished"
        }

        success {
            echo "Deployment completed successfully"
        }

        unstable {
            echo "Build unstable due to test failures"
        }

        failure {
            echo "Pipeline failed"
        }

    }
}
```

---

# 2. Pipeline Execution Flow

```
Pipeline Trigger
      ↓
Checkout Code
      ↓
Build Application
      ↓
Tests + Sonar Scan (Parallel)
      ↓
Build Docker Image
      ↓
Push Docker Image
      ↓
Production Approval
      ↓
Deploy to Kubernetes
      ↓
Post Actions
```

---

# 3. Explanation of Important Blocks

---

# 3.1 `parameters` Block

This block allows **user input when triggering the pipeline**.

```
parameters {
    string(...)
    choice(...)
    booleanParam(...)
}
```

### Parameters used

| Parameter   | Type    | Purpose              |
| ----------- | ------- | -------------------- |
| BRANCH_NAME | string  | Git branch to build  |
| DEPLOY_ENV  | choice  | Environment          |
| RUN_TESTS   | boolean | Enable/disable tests |

Example when triggering pipeline:

```
BRANCH_NAME = develop
DEPLOY_ENV = uat
RUN_TESTS = true
```

Access parameter:

```
params.BRANCH_NAME
params.DEPLOY_ENV
```

---

# 3.2 `triggers` Block

```
triggers {
    pollSCM('H/5 * * * *')
}
```

Meaning:

```
Every 5 minutes Jenkins checks Git repository.
```

If new commit is found → pipeline starts.

---

# 3.3 `checkout`

```
checkout([
$class: 'GitSCM',
branches: [[name: "*/${params.BRANCH_NAME}"]],
userRemoteConfigs: [[
url: 'https://github.com/example/payment-service.git'
]]
])
```

Purpose:

```
Download code from Git repository into Jenkins workspace.
```

Workspace example:

```
/var/lib/jenkins/workspace/payment-service
```

---

# 3.4 `retry(3)`

```
retry(3) {
    sh 'mvn clean package'
}
```

If command fails Jenkins retries **3 times**.

Example:

```
Attempt 1 → Failed
Attempt 2 → Failed
Attempt 3 → Success
```

Used when failure happens due to:

```
network issue
dependency download failure
temporary build failure
```

---

# 3.5 `when` Block

Controls **whether stage should execute**.

Example:

```
when {
    expression {
        params.RUN_TESTS == true
    }
}
```

Meaning:

```
Run stage only if RUN_TESTS = true
```

---

Another example:

```
when {
    environment name: 'DEPLOY_ENV', value: 'prod'
}
```

Meaning:

```
Run stage only if environment = prod
```

---

# 3.6 `parallel` Block

Runs multiple stages **simultaneously**.

```
parallel {

    stage('Unit Tests')

    stage('SonarQube Scan')

}
```

Execution:

```
Build
   ↓
 ┌─────────────┬─────────────┐
Unit Tests   Sonar Scan
```

This reduces pipeline time.

---

# 3.7 `catchError`

```
catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE')
```

Behavior:

| Condition          | Result         |
| ------------------ | -------------- |
| Tests fail         | Stage = FAILED |
| Pipeline           | UNSTABLE       |
| Pipeline continues | Yes            |

Example pipeline result:

```
Build → SUCCESS
Tests → FAILURE
Pipeline → UNSTABLE
```

Why used?

```
Do not stop deployment due to test failure.
```

---

# 3.8 Docker Build

```
docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
```

Example result:

```
nikhilsy/payment-service:24
```

Where

```
BUILD_NUMBER = Jenkins build id
```

Automatically generated by Jenkins.

---

# 3.9 Docker Push

```
docker push repo:tag
```

Example:

```
docker push nikhilsy/payment-service:24
```

Image stored in:

```
DockerHub Registry
```

---

# 3.10 Approval Stage

```
input message: "Approve deployment?"
```

Pipeline pauses until user clicks:

```
Proceed
Abort
```

Used for **production deployments**.

---

# 3.11 Kubernetes Deployment

```
kubectl set image deployment/app app=image
```

Example:

```
kubectl set image deployment/payment-service \
payment-service=nikhilsy/payment-service:24
```

Effect:

```
Old Pod → Terminated
New Pod → Created with new image
```

---

# 3.12 `post` Block

Runs **after pipeline completes**.

```
post {
    always
    success
    unstable
    failure
}
```

Example behavior

| Result   | Action                |
| -------- | --------------------- |
| success  | Deployment successful |
| unstable | Test failure          |
| failure  | Build failure         |

---

# 4. Final Real DevOps CI/CD Architecture

```
Developer
   ↓
GitHub Commit
   ↓
Jenkins Trigger
   ↓
Checkout Code
   ↓
Build (Maven)
   ↓
Tests + Sonar Scan
   ↓
Docker Build
   ↓
DockerHub Push
   ↓
Manual Approval
   ↓
Kubernetes Deployment
```

---

✅ Since you are already **2+ years DevOps Engineer**, the **next very important Jenkins concepts used in production pipelines** are:

1️⃣ **stash vs archiveArtifacts vs artifacts in Jenkins**
2️⃣ **workspace vs Jenkins home vs build directory**
3️⃣ **how Jenkins schedules pipelines on agents internally**
4️⃣ **why Jenkins builds fail even when agent is healthy**
5️⃣ **how multi-branch pipelines work internally**

These are **very common real troubleshooting interview questions**.


################################Sonar quality check###################################################

Below is a **complete improved Jenkins Declarative Pipeline** including everything you asked:

* `parameters`
* `triggers`
* `checkout`
* `parallel`
* `retry`
* `when`
* `catchError`
* `manual approval`
* `Docker build & push`
* `Kubernetes deployment`
* `post actions`

After the pipeline, I will **explain every block and command clearly**.

---

# 1. Complete CI/CD Jenkins Pipeline

```groovy
pipeline {

    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Git branch to build')
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'uat', 'prod'], description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run unit tests')
    }

    environment {
        APP_NAME = "payment-service"
        DOCKER_REPO = "nikhilsy/payment-service"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH_NAME}"]],
                    userRemoteConfigs: [[
                        url: 'https://github.com/example/payment-service.git'
                    ]]
                ])
            }
        }

        stage('Build Application') {
            steps {
                retry(3) {
                    sh 'mvn clean package'
                }
            }
        }

        stage('Tests and Code Scan') {

            when {
                expression {
                    params.RUN_TESTS == true
                }
            }

            parallel {

                stage('Unit Tests') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            sh 'mvn test'
                        }
                    }
                }

                stage('SonarQube Scan') {
                    steps {
                        sh 'mvn sonar:sonar'
                    }
                }

            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
                """
            }
        }

        stage('Push Docker Image') {

            when {
                anyOf {
                    environment name: 'DEPLOY_ENV', value: 'uat'
                    environment name: 'DEPLOY_ENV', value: 'prod'
                }
            }

            steps {
                sh """
                docker push ${DOCKER_REPO}:${BUILD_NUMBER}
                """
            }
        }

        stage('Approval for Production') {

            when {
                environment name: 'DEPLOY_ENV', value: 'prod'
            }

            steps {
                input message: "Approve deployment to Production?"
            }
        }

        stage('Deploy to Kubernetes') {

            when {
                anyOf {
                    environment name: 'DEPLOY_ENV', value: 'uat'
                    environment name: 'DEPLOY_ENV', value: 'prod'
                }
            }

            steps {
                sh """
                kubectl set image deployment/${APP_NAME} \
                ${APP_NAME}=${DOCKER_REPO}:${BUILD_NUMBER}
                """
            }
        }

    }

    post {

        always {
            echo "Pipeline execution finished"
        }

        success {
            echo "Deployment completed successfully"
        }

        unstable {
            echo "Build unstable due to test failures"
        }

        failure {
            echo "Pipeline failed"
        }

    }
}
```

---

# 2. Pipeline Execution Flow

```
Pipeline Trigger
      ↓
Checkout Code
      ↓
Build Application
      ↓
Tests + Sonar Scan (Parallel)
      ↓
Build Docker Image
      ↓
Push Docker Image
      ↓
Production Approval
      ↓
Deploy to Kubernetes
      ↓
Post Actions
```

---

# 3. Explanation of Important Blocks

---

# 3.1 `parameters` Block

This block allows **user input when triggering the pipeline**.

```
parameters {
    string(...)
    choice(...)
    booleanParam(...)
}
```

### Parameters used

| Parameter   | Type    | Purpose              |
| ----------- | ------- | -------------------- |
| BRANCH_NAME | string  | Git branch to build  |
| DEPLOY_ENV  | choice  | Environment          |
| RUN_TESTS   | boolean | Enable/disable tests |

Example when triggering pipeline:

```
BRANCH_NAME = develop
DEPLOY_ENV = uat
RUN_TESTS = true
```

Access parameter:

```
params.BRANCH_NAME
params.DEPLOY_ENV
```

---

# 3.2 `triggers` Block

```
triggers {
    pollSCM('H/5 * * * *')
}
```

Meaning:

```
Every 5 minutes Jenkins checks Git repository.
```

If new commit is found → pipeline starts.

---

# 3.3 `checkout`

```
checkout([
$class: 'GitSCM',
branches: [[name: "*/${params.BRANCH_NAME}"]],
userRemoteConfigs: [[
url: 'https://github.com/example/payment-service.git'
]]
])
```

Purpose:

```
Download code from Git repository into Jenkins workspace.
```

Workspace example:

```
/var/lib/jenkins/workspace/payment-service
```

---

# 3.4 `retry(3)`

```
retry(3) {
    sh 'mvn clean package'
}
```

If command fails Jenkins retries **3 times**.

Example:

```
Attempt 1 → Failed
Attempt 2 → Failed
Attempt 3 → Success
```

Used when failure happens due to:

```
network issue
dependency download failure
temporary build failure
```

---

# 3.5 `when` Block

Controls **whether stage should execute**.

Example:

```
when {
    expression {
        params.RUN_TESTS == true
    }
}
```

Meaning:

```
Run stage only if RUN_TESTS = true
```

---

Another example:

```
when {
    environment name: 'DEPLOY_ENV', value: 'prod'
}
```

Meaning:

```
Run stage only if environment = prod
```

---

# 3.6 `parallel` Block

Runs multiple stages **simultaneously**.

```
parallel {

    stage('Unit Tests')

    stage('SonarQube Scan')

}
```

Execution:

```
Build
   ↓
 ┌─────────────┬─────────────┐
Unit Tests   Sonar Scan
```

This reduces pipeline time.

---

# 3.7 `catchError`

```
catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE')
```

Behavior:

| Condition          | Result         |
| ------------------ | -------------- |
| Tests fail         | Stage = FAILED |
| Pipeline           | UNSTABLE       |
| Pipeline continues | Yes            |

Example pipeline result:

```
Build → SUCCESS
Tests → FAILURE
Pipeline → UNSTABLE
```

Why used?

```
Do not stop deployment due to test failure.
```

---

# 3.8 Docker Build

```
docker build -t ${DOCKER_REPO}:${BUILD_NUMBER} .
```

Example result:

```
nikhilsy/payment-service:24
```

Where

```
BUILD_NUMBER = Jenkins build id
```

Automatically generated by Jenkins.

---

# 3.9 Docker Push

```
docker push repo:tag
```

Example:

```
docker push nikhilsy/payment-service:24
```

Image stored in:

```
DockerHub Registry
```

---

# 3.10 Approval Stage

```
input message: "Approve deployment?"
```

Pipeline pauses until user clicks:

```
Proceed
Abort
```

Used for **production deployments**.

---

# 3.11 Kubernetes Deployment

```
kubectl set image deployment/app app=image
```

Example:

```
kubectl set image deployment/payment-service \
payment-service=nikhilsy/payment-service:24
```

Effect:

```
Old Pod → Terminated
New Pod → Created with new image
```

---

# 3.12 `post` Block

Runs **after pipeline completes**.

```
post {
    always
    success
    unstable
    failure
}
```

Example behavior

| Result   | Action                |
| -------- | --------------------- |
| success  | Deployment successful |
| unstable | Test failure          |
| failure  | Build failure         |

---

# 4. Final Real DevOps CI/CD Architecture

```
Developer
   ↓
GitHub Commit
   ↓
Jenkins Trigger
   ↓
Checkout Code
   ↓
Build (Maven)
   ↓
Tests + Sonar Scan
   ↓
Docker Build
   ↓
DockerHub Push
   ↓
Manual Approval
   ↓
Kubernetes Deployment
```

---

I’ll explain this in **DevOps interview style** so it’s easy to remember.

These terms come from **static code analysis tools** like **SonarQube**, which analyze source code without running it.

---

# 1. What is Static Code Analysis?

### Definition

Static code analysis is the process of **analyzing source code to detect quality issues, bugs, and security problems without executing the program**.

Example tools:

* SonarQube
* ESLint
* Checkstyle

In DevOps pipelines, static analysis is usually executed **after build and before deployment**.

---

# 2. Bugs

### Definition

A **bug** is a coding mistake that causes the program to behave incorrectly or crash.

These are **logical or programming errors**.

### Example

```java
int a = 10;
int b = 0;

int result = a / b;
```

Problem:

```
Division by zero
```

This will cause:

```
ArithmeticException
```

So **SonarQube marks this as a bug**.

---

### Real Production Example

```java
if(user == null)
    user.getName();
```

This will cause:

```
NullPointerException
```

Bug severity levels usually are:

| Severity | Meaning             |
| -------- | ------------------- |
| Blocker  | Application crash   |
| Critical | Major runtime issue |
| Major    | Functional issue    |
| Minor    | Small issue         |

---

# 3. Code Smell

### Definition

A **code smell** is a design or coding pattern that **does not break the application but makes the code hard to maintain, read, or extend**.

Code smells are **bad programming practices**.

---

### Example 1 — Duplicate Code

```java
if(role.equals("ADMIN")){
   sendNotification();
}

if(role.equals("USER")){
   sendNotification();
}
```

This is duplicate logic.

Better solution:

```java
sendNotification();
```

---

### Example 2 — Very Large Method

Bad code:

```java
public void processOrder(){

  // 200 lines of code

}
```

Good code:

```
processOrder()
   ├ validateOrder()
   ├ calculatePrice()
   └ saveOrder()
```

---

### Example 3 — Hardcoded values

Bad practice

```java
int timeout = 5000;
```

Better

```java
int timeout = config.getTimeout();
```

---

### Why code smell is important

Even if the application runs correctly:

```
Code becomes difficult to maintain
Hard to debug
Hard to scale
```

So **SonarQube reports code smells**.

---

# 4. Security Vulnerabilities

### Definition

A **security vulnerability is a weakness in code that attackers can exploit**.

These are **security risks in the application**.

---

### Example 1 — SQL Injection

Bad code

```java
String query = "SELECT * FROM users WHERE name = '" + username + "'";
```

If attacker enters

```
' OR '1'='1
```

Query becomes

```
SELECT * FROM users WHERE name='' OR '1'='1'
```

This returns **all database records**.

Correct solution

```java
PreparedStatement stmt = conn.prepareStatement(
"SELECT * FROM users WHERE name=?");
```

---

### Example 2 — Hardcoded password

Bad code

```java
String password = "admin123";
```

This is a **security vulnerability**.

---

### Example 3 — Weak encryption

Using weak algorithms like

```
MD5
SHA1
```

Instead use

```
SHA-256
bcrypt
```

---

### Vulnerability severity

| Level    | Meaning                 |
| -------- | ----------------------- |
| Critical | Immediate security risk |
| High     | Serious vulnerability   |
| Medium   | Moderate risk           |
| Low      | Minor issue             |

---

# 5. Code Coverage

### Definition

Code coverage measures **how much of the application code is tested by automated tests**.

It is usually measured in **percentage**.

---

### Example

Application code

```
100 lines of code
```

Test cases cover

```
70 lines
```

Coverage

```
70%
```

---

### Example

Code:

```java
if(user.isActive()){
   sendEmail();
}
```

If test case only tests:

```
user active
```

But not

```
user inactive
```

Coverage is incomplete.

---

### Types of coverage

| Type              | Meaning               |
| ----------------- | --------------------- |
| Line Coverage     | Lines executed        |
| Branch Coverage   | Decision paths tested |
| Function Coverage | Functions tested      |

---

### Good coverage percentage

| Coverage | Quality |
| -------- | ------- |
| < 50%    | Poor    |
| 50–70%   | Average |
| 70–85%   | Good    |

> 85% | Excellent |

---

# 6. What `mvn sonar:sonar` Does

### Definition

`mvn sonar:sonar` runs **code quality analysis using SonarQube**.

It sends code analysis results to the **SonarQube server.

---

### Pipeline command

```bash
mvn sonar:sonar
```

---

### Internal process

```
Source Code
     ↓
Maven Build
     ↓
Sonar Scanner
     ↓
Send report to SonarQube Server
     ↓
Quality Dashboard
```

---

### What Sonar analyzes

It checks for:

```
bugs
code smells
security vulnerabilities
test coverage
duplication
complexity
```

---

### Example Jenkins stage

```groovy
stage('SonarQube Scan') {
    steps {
        sh 'mvn sonar:sonar'
    }
}
```

---

### Output in Sonar Dashboard

Example result

```
Bugs: 2
Code Smells: 15
Vulnerabilities: 1
Coverage: 78%
```

---

# 7. What Happens If Sonar Quality Gate Fails

Many pipelines enforce **Quality Gate**.

Example rule:

```
Coverage must be > 80%
No critical vulnerabilities
```

If rule fails

```
Pipeline fails
Deployment blocked
```

This ensures **only high-quality code goes to production**.

---

# 8. Real DevOps Pipeline with Sonar

```
Developer Push Code
        ↓
Jenkins Trigger
        ↓
Build (Maven)
        ↓
Unit Tests
        ↓
SonarQube Scan
        ↓
Quality Gate Check
        ↓
Docker Build
        ↓
Deploy
```

---

✅ Since you are learning **DevOps pipelines deeply**, the **next very important topic** is:

**How SonarQube integrates with Jenkins internally**

This includes:

* `withSonarQubeEnv`
* Sonar Scanner
* Quality Gate check
* `waitForQualityGate`

These are **extremely common in DevOps interviews** and real CI/CD pipelines.
