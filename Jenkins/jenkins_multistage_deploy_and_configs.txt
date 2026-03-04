---

# Multiple Environment Build in Jenkins

## ✅ What is Multiple Environment Build?

It means:

> Using a single Jenkins pipeline to build once and deploy the same artifact to multiple environments like:

* INT (Integration)
* UAT (User Acceptance Testing)
* PROD (Production)

This ensures:

* Same artifact across environments
* No rebuild for each stage
* Proper promotion strategy

---

# ✅ Approach (Best Practice)

### 🔹 Build Once → Deploy Multiple Times

```
Code → Build → Artifact → Deploy to INT → Deploy to UAT → Deploy to PROD
```

---

# ✅ Sample Declarative Jenkinsfile

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['INT', 'UAT', 'PROD'], description: 'Select Environment')
    }

    environment {
        APP_NAME = "my-app"
        ARTIFACT = "target/my-app.jar"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo.git'
            }
        }

        stage('Build') {
            when {
                expression { params.ENV == 'INT' }
            }
            steps {
                sh 'mvn clean package'
                archiveArtifacts artifacts: "${ARTIFACT}", fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                script {
                    if (params.ENV == 'INT') {
                        sh 'echo Deploying to INT server'
                    }
                    else if (params.ENV == 'UAT') {
                        sh 'echo Deploying to UAT server'
                    }
                    else if (params.ENV == 'PROD') {
                        sh 'echo Deploying to PROD server'
                    }
                }
            }
        }
    }
}
```

---

# ✅ Better Production-Ready Version (Recommended)

Instead of using `if-else`, use **separate stages with conditions**.

```groovy
pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                sh 'mvn clean package'
                stash name: 'app', includes: 'target/*.jar'
            }
        }

        stage('Deploy to INT') {
            when { branch 'develop' }
            steps {
                unstash 'app'
                sh 'echo Deploying to INT'
            }
        }

        stage('Deploy to UAT') {
            when { branch 'release' }
            steps {
                unstash 'app'
                sh 'echo Deploying to UAT'
            }
        }

        stage('Deploy to PROD') {
            when { branch 'main' }
            steps {
                unstash 'app'
                sh 'echo Deploying to PROD'
            }
        }
    }
}
```

---

# ✅ Real-Time Enterprise Example (Like Your Project)

Since you mentioned earlier:

* You use **GoCD**
* Build tool is **Gradle**
* Canary deployment is used
* Environments: INT → UAT → PROD

In such setup:

### 🔹 Stage Flow:

```
Checkout
Build (gradle build)
SonarQube Scan
Publish Artifact (Nexus/Artifactory)
Deploy INT
Manual Approval
Deploy UAT
Canary Deployment PROD
Full Rollout
```

---

# ✅ Advanced Version (Using Environment Variables Per Env)

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['INT','UAT','PROD'])
    }

    environment {
        INT_SERVER  = "10.10.1.10"
        UAT_SERVER  = "10.10.2.10"
        PROD_SERVER = "10.10.3.10"
    }

    stages {

        stage('Build') {
            steps {
                sh 'gradle build'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def server = ""

                    if (params.ENV == "INT") {
                        server = env.INT_SERVER
                    } else if (params.ENV == "UAT") {
                        server = env.UAT_SERVER
                    } else {
                        server = env.PROD_SERVER
                    }

                    sh "echo Deploying to ${server}"
                }
            }
        }
    }
}
```

---

# ✅ Interview Answer (Short Version)

If interviewer asks:

> How do you handle multi-environment deployment in Jenkins?

You can say:

> We follow a build-once-deploy-many strategy. The pipeline builds the artifact only once and stores it in an artifact repository. Based on branch or parameter selection, the pipeline deploys the same artifact sequentially to INT, UAT, and PROD environments with approval gates before production.

---
###########################Config files############################
---


Good question Nikhil 👍
This is **very important in real DevOps projects**, especially since you work across **INT → UAT → PROD** environments.

I’ll explain in **interview-style structured format** as you prefer.

---

# ✅ What Are Config Files?

## Definition

> Configuration files store environment-specific values like database URLs, API endpoints, ports, credentials references, feature flags, etc., without changing application code.

They allow:

* Same code
* Same artifact
* Different behavior per environment

---

# ✅ Why We Use Config Files?

### Problem Without Config Files

If you hardcode values:

```properties
db.url=jdbc:mysql://int-db:3306/app
```

You must rebuild for UAT and PROD ❌
This breaks **Build Once Deploy Many** principle.

---

### Solution

Externalize configs:

```properties
db.url=${DB_URL}
```

Now you only change environment variables, not code ✅

---

# ✅ Where Do We Store Config Files?

There are **4 common places** in enterprise projects:

---

## 1️⃣ Inside Application (Not Recommended for PROD)

Example:

```
application-int.properties
application-uat.properties
application-prod.properties
```

Used in:

* Small projects
* Non-cloud apps

Problem:

* Still bundled inside artifact
* Less flexible

---

## 2️⃣ On Server (External Config Directory) ✅ Common

Example:

```
/opt/myapp/config/application-prod.properties
```

Jenkins deploys:

* Artifact (.jar/.war)
* Config file separately

App runs like:

```bash
java -jar app.jar --spring.config.location=/opt/myapp/config/
```

✔ Same jar
✔ Different config per environment

---

## 3️⃣ Environment Variables (Cloud Native Way) ✅ Recommended

Very common in:

* Kubernetes
* Docker
* Cloud deployments

Example in Jenkins:

```groovy
environment {
    DB_URL = credentials('prod-db-url')
}
```

In app:

```properties
db.url=${DB_URL}
```

Used heavily in containerized apps.

---

## 4️⃣ Configuration Management Tools (Enterprise Level)

Examples:

* HashiCorp Consul
* Spring Cloud Config
* AWS Systems Manager Parameter Store
* AWS Secrets Manager

Best for:

* Microservices
* Large-scale systems
* Secure secret storage

---

# ✅ How Jenkins Uses Config Files

## Method 1: Use Jenkins Credentials

Store in Jenkins:

* DB password
* API keys
* SSH keys

Use in Jenkinsfile:

```groovy
withCredentials([string(credentialsId: 'prod-db-pass', variable: 'DB_PASS')]) {
    sh 'echo $DB_PASS'
}
```

---

## Method 2: Config File Provider Plugin

Jenkins plugin:
👉 **Managed Files**

You upload config file in Jenkins UI.

Then in pipeline:

```groovy
configFileProvider([configFile(fileId: 'prod-config', variable: 'CONFIG_FILE')]) {
    sh 'cp $CONFIG_FILE application.properties'
}
```

Good for:

* Shared configs
* Controlled updates

---

## Method 3: Kubernetes ConfigMap (Modern Way)

If deploying to Kubernetes:

* Non-sensitive → ConfigMap
* Sensitive → Secret

Example:

```yaml
env:
  - name: DB_URL
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: db_url
```

---

# ✅ Real Example Based on Your Environment (INT → UAT → PROD)

Let’s say:

| Environment | DB URL                |
| ----------- | --------------------- |
| INT         | int-db.company.local  |
| UAT         | uat-db.company.local  |
| PROD        | prod-db.company.local |

You should:

1. Store DB URLs in environment-specific config
2. Jenkins selects config based on ENV parameter
3. Same artifact deployed everywhere

---

# ✅ Production-Ready Pattern (Best Practice)

### 🔥 Follow This Rule:

```text
Code → Build → Artifact → Inject Config at Runtime → Deploy
```

NOT:

```text
Code → Change Config → Rebuild → Deploy
```

---

# ✅ Interview Answer (Short & Strong)

If interviewer asks:

> How do you manage configuration across environments?

You can say:

> We externalize configuration from application code. Environment-specific values like database URLs and API endpoints are stored either as environment variables, external config files, or secret management systems. Jenkins injects these values at deployment time, ensuring we follow build-once-deploy-many principle and avoid rebuilding artifacts per environment.

---

# ✅ Important DevOps Best Practices

Since you’re targeting higher DevOps roles:

* Never store secrets in Git
* Use Jenkins Credentials
* Use secret managers in cloud
* Separate sensitive & non-sensitive configs
* Version control non-sensitive configs
* Encrypt secrets

---
