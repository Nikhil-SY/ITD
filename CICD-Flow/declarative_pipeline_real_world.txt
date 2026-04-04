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