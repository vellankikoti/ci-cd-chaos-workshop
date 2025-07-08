# 🚀 Scenario 02 — Testcontainers Chaos Showdown

> **Operation Chaos**  
> The Chaos Agent is trying to sabotage our pipelines by creating flaky integration tests!  
> Our mission: fight back using Testcontainers and prove that containerized testing is bulletproof.

---

## 🎯 Scenario Goal

✅ Learn how to:
- Write **integration tests** with Python and Testcontainers
- Run Postgres and Redis containers dynamically during tests
- Simulate pipeline failures and fixes
- Integrate tests into a Jenkins pipeline
- Build confidence handling **Chaos Agent’s sabotage!**

---

## 🛠️ Technical Stack

- **Python 3.12+**
- **pytest**
- **Testcontainers Python**
- **Docker**
- **Jenkins**

---

## 📂 Project Structure

```

scenario\_02\_testcontainers/
├── Dockerfile
├── requirements.txt
└── tests/
├── test\_postgres\_pass.py
├── test\_postgres\_fail.py
├── test\_redis\_pass.py
└── test\_redis\_fail.py

````

---

## 🚀 How It Works

### ✅ Postgres Passing Test

- Spins up a **Postgres 15** container
- Connects via psycopg2
- Runs a simple query:
    ```sql
    SELECT version();
    ```
- Confirms Postgres responds successfully.

See:
````

tests/test\_postgres\_pass.py

```

---

### ❌ Postgres Failing Test

- Spins up a Postgres container
- Deliberately uses the **wrong password**
- Expects a connection failure

Chaos Agent strikes…but we predict it!

See:
```

tests/test\_postgres\_fail.py

```

---

### ✅ Redis Passing Test

- Spins up a **Redis 7** container
- Connects via redis-py
- Stores and retrieves a value

See:
```

tests/test\_redis\_pass.py

```

---

### ❌ Redis Failing Test

- Spins up Redis
- Tries connecting on the **wrong port**
- Expects a connection failure

Chaos Agent’s sabotage detected!

See:
```

tests/test\_redis\_fail.py

````

---

## ⚙️ Running Tests Locally

**1. Build the Docker image:**

```bash
docker build -t ci-cd-chaos-python:latest .
````

**2. Run tests:**

✅ Run all passing tests:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd):/workspace \
    -w /workspace \
    ci-cd-chaos-python:latest \
    pytest Jenkins/jenkins_scenarios/scenario_02_testcontainers/tests/test_postgres_pass.py \
           Jenkins/jenkins_scenarios/scenario_02_testcontainers/tests/test_redis_pass.py
```

❌ Run failing tests (Chaos simulation):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    -v $(pwd):/workspace \
    -w /workspace \
    ci-cd-chaos-python:latest \
    pytest Jenkins/jenkins_scenarios/scenario_02_testcontainers/tests/test_postgres_fail.py \
           Jenkins/jenkins_scenarios/scenario_02_testcontainers/tests/test_redis_fail.py
```

---

## ⚙️ Running Tests in Jenkins

### Parameters:

* `TEST_MODE`:

  * `pass` → run passing tests
  * `fail` → run chaos-induced failing tests

✅ Jenkins Pipeline Example:

```groovy
pipeline {
    agent {
        docker {
            image 'ci-cd-chaos-python:latest'
            args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        TESTCONTAINERS_RYUK_DISABLED = 'true'
    }

    parameters {
        choice(
            name: 'TEST_MODE',
            choices: ['fail', 'pass'],
            description: 'Run failing tests or fixed tests?'
        )
    }

    stages {
        ...
    }
}
```

✅ Jenkins automatically:

* Clones the repo
* Installs Python dependencies
* Runs chosen tests
* Shows pipeline green or red

---

## 🤯 Chaos Agent’s Tricks

Chaos Agent might:

* Block docker networking
* Break credentials
* Trigger connection errors

…but our pipeline will **detect and defeat** these attacks!

---

## ✅ Victory Condition

✨ You’ve defeated Chaos Agent if:

* **Passing tests succeed** in Jenkins
* **Failing tests fail intentionally** in Jenkins
* Your pipeline is **predictable and robust**

---

## 👊 Remember:

> **“Chaos is only chaos until it’s tested.”**
> — CI/CD Chaos Workshop

Go forth and slay Chaos Agent! 🎉

```

---
