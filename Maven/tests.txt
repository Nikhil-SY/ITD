Maven identifies **Unit Tests vs Integration Tests mainly using naming conventions and plugins**.

---

# 1. Unit Test Identification in Maven

Maven runs **unit tests during the `test` phase** using:

```text
maven-surefire-plugin
```

### Default Naming Patterns (Unit Tests)

Maven treats files as **unit tests** if their names match these patterns:

```
Test*.java
*Test.java
*Tests.java
*TestCase.java
```

### Example

```
UserServiceTest.java
TestPaymentService.java
OrderTests.java
```

Location:

```
src/test/java
```

These are executed when you run:

```
mvn test
```

or

```
mvn clean package
```

---

# 2. Integration Test Identification in Maven

Integration tests are executed **after packaging** using:

```
maven-failsafe-plugin
```

### Default Naming Patterns (Integration Tests)

```
IT*.java
*IT.java
*ITCase.java
```

### Example

```
UserServiceIT.java
DatabaseConnectionIT.java
PaymentITCase.java
```

These are executed during:

```
integration-test
verify
```

Command:

```
mvn verify
```

---

# 3. Lifecycle Difference

### Unit Tests

Run in **test phase**

```
validate
compile
test-compile
test  ← Unit tests executed
```

---

### Integration Tests

Run after packaging

```
package
integration-test  ← Integration tests run
verify
```

---

# 4. Plugins Responsible

| Test Type        | Plugin                | Lifecycle Phase               |
| ---------------- | --------------------- | ----------------------------- |
| Unit Test        | Maven Surefire Plugin | `test`                        |
| Integration Test | Maven Failsafe Plugin | `integration-test` / `verify` |

---

# 5. Example Project Structure

```
project
 ├── src
 │   ├── main/java
 │   └── test/java
 │        ├── UserServiceTest.java   (Unit Test)
 │        └── UserServiceIT.java     (Integration Test)
 └── pom.xml
```

---

# 6. Why Maven Separates Them

**Unit Tests**

* Fast
* Test individual classes
* No external dependencies

**Integration Tests**

* Slower
* Test DB, APIs, services
* Need environment setup

Example:

```
Unit Test → Test Java method
Integration Test → Test DB + API + Application
```

---

# 7. Interview Style Answer

**Question:** How does Maven differentiate unit tests and integration tests?

**Answer:**

Maven differentiates them mainly through **naming conventions and plugins**.
Unit tests are executed during the **test phase** using the **Maven Surefire Plugin** and usually follow naming patterns like `*Test.java`.
Integration tests are executed later during the **integration-test and verify phases** using the **Maven Failsafe Plugin**, and they follow naming patterns like `*IT.java`.

---

✅ **Common DevOps interview follow-up question**

**Why do we use `Failsafe plugin` for integration tests instead of `Surefire`?**

Because **Failsafe allows the build to finish packaging before running integration tests and handles failures differently**, ensuring proper cleanup.

---

If you want, I can also explain **the exact difference between `mvn test`, `mvn verify`, and `mvn install`**, which is **one of the most asked Maven questions in DevOps interviews**.

##############################################################################################################

