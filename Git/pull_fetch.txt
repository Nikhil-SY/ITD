# 🟢 First: What Is `origin`?

When you clone from
GitHub

```bash
git clone https://github.com/org/repo.git
```

Git automatically creates a remote called:

```
origin
```

You can check:

```bash
git remote -v
```

---

# 🟢 Git Fetch

## 🔹 Command

```bash
git fetch origin
```

---

## 🔹 What It Does

✔ Connects to remote (GitHub)
✔ Downloads latest commits
✔ Updates remote-tracking branch
✔ DOES NOT modify your local branch

---

## 🔹 What Actually Happens Internally

Imagine:

Remote main:

```
A---B---C---D
```

Your local main:

```
A---B---C
```

You run:

```bash
git fetch origin
```

Now Git updates:

```
origin/main → D
```

But your local branch is still:

```
main → C
```

Nothing changes in your working directory.

---

## 🔹 Why Use Fetch?

* To see changes before merging
* Safe way to inspect remote updates
* Avoid automatic merge conflicts

You can compare:

```bash
git diff main origin/main
```

---

# 🟢 Git Pull

## 🔹 Command

```bash
git pull origin main
```

---

## 🔹 What It Does

Git Pull = Fetch + Merge

Internally it does:

```bash
git fetch origin
git merge origin/main
```

---

## 🔹 What Happens Visually

Before:

Local:

```
A---B---C
```

Remote:

```
A---B---C---D
```

After pull:

```
A---B---C---D
```

Your branch updates automatically.

---

# 🟡 What If You Have Local Changes?

Local:

```
A---B---C---E
```

Remote:

```
A---B---C---D
```

If you do:

```bash
git pull
```

Git will create a merge commit:

```
        E
       /
A---B---C---D
       \
        M
```

That’s why sometimes history becomes messy.

---

# 🟢 What Is `git pull --rebase`?

Instead of merge:

```bash
git pull --rebase origin main
```

It does:

* Fetch
* Reapply your local commits on top of remote

Result:

```
A---B---C---D---E
```

Clean linear history.

Preferred in many teams.

---

# 🟢 When To Use What?

### Use `git fetch` when:

* You want control
* You want to inspect changes
* You don’t want auto merge

### Use `git pull` when:

* You just want latest code quickly
* No local changes

### Use `git pull --rebase` when:

* You want clean history
* Team follows rebase strategy

---

# 🔥 Interview-Level Answer

If interviewer asks:

> What is difference between git fetch and git pull?

Answer:

> Git fetch downloads changes from the remote repository without modifying the current branch, whereas git pull performs a fetch followed by a merge (or rebase) into the current branch.

That’s precise and correct.

---

# 🧠 Now Let Me Clear One Common Confusion

After `git fetch`, why does your code not change?

Because fetch updates only:

```
.git/refs/remotes/origin/main
```

Not your working directory.

