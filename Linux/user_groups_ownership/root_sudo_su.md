## ✅ Difference Between `sudo`, `root`, and `su`

(Interview-Style Explanation)

---

# 🎯 1️⃣ `root` User

### 📌 What is root?

* Superuser account
* UID = 0
* Has **unrestricted access** to entire system

### Example:

```bash
whoami
root
```

### Key Point:

> Root is a **user account**, not a command.

---

# 🎯 2️⃣ `sudo` (Superuser Do)

### 📌 What is sudo?

* Command to execute a **single command as another user (default: root)**
* Requires your own password (if configured)

### Example:

```bash
sudo systemctl restart nginx
```

### Behavior:

* Executes only that command as root
* Logs activity in `/var/log/auth.log` or `/var/log/secure`
* Controlled by `/etc/sudoers`

### Key Concept:

> Temporary privilege escalation

---

# 🎯 3️⃣ `su` (Switch User)

### 📌 What is su?

* Switches from current user to another user (default: root)
* Requires **target user’s password**

### Example:

```bash
su -
```

* Opens a full root shell session

Exit with:

```bash
exit
```

---

# 🔎 Comparison Table

| Feature               | sudo          | su            | root         |
| --------------------- | ------------- | ------------- | ------------ |
| Type                  | Command       | Command       | User         |
| Password required     | Your password | Root password | N/A          |
| Access duration       | One command   | Full session  | Full session |
| Logging               | Yes           | Minimal       | N/A          |
| Secure for production | ✅ Yes         | ⚠ Less secure | ⚠ Risky      |

---

# 🚀 Real DevOps Best Practice

✔ Prefer `sudo` over `su`
✔ Disable direct root login (`PermitRootLogin no`)
✔ Avoid sharing root password
✔ Use role-based sudo access

---

# 🎯 Important Difference (Interview Highlight)

> `sudo` → Controlled, logged, command-level access
> `su` → Full shell access, less controlled

---

# 🎤 Follow-up Question

**Q: What is the difference between `su` and `su -`?**

👉 `su -` loads the target user's environment (like full login).
👉 `su` keeps current environment variables.

---