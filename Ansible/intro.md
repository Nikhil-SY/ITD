# Ansible: The Complete Guide (Zero to Advanced)

> A comprehensive reference covering Ansible from first principles to production-grade automation — installation, core concepts, playbooks, roles, Vault, dynamic inventory (AWS), and CI/CD integration.

---

## Table of Contents

1. [Introduction — What, Why, How](#1-introduction--what-why-how)
2. [Installation](#2-installation)
3. [Core Architecture & Concepts](#3-core-architecture--concepts)
4. [YAML Primer](#4-yaml-primer)
5. [Inventory](#5-inventory)
6. [Ad-Hoc Commands](#6-ad-hoc-commands)
7. [Playbooks](#7-playbooks)
8. [Variables, Facts & Precedence](#8-variables-facts--precedence)
9. [Conditionals & Loops](#9-conditionals--loops)
10. [Handlers & Notifications](#10-handlers--notifications)
11. [Templates (Jinja2)](#11-templates-jinja2)
12. [Roles](#12-roles)
13. [Ansible Galaxy & Collections](#13-ansible-galaxy--collections)
14. [Ansible Vault (Secrets Management)](#14-ansible-vault-secrets-management)
15. [Error Handling & Blocks](#15-error-handling--blocks)
16. [Tags](#16-tags)
17. [Dynamic Inventory (AWS Example)](#17-dynamic-inventory-aws-example)
18. [Ansible + AWS (Provisioning Example)](#18-ansible--aws-provisioning-example)
19. [Directory Structure & Best Practices](#19-directory-structure--best-practices)
20. [CI/CD Integration](#20-cicd-integration)
21. [Troubleshooting Guide](#21-troubleshooting-guide)
22. [Command Cheat Sheet](#22-command-cheat-sheet)

---

## 1. Introduction — What, Why, How

### What is Ansible?

Ansible is an **open-source automation tool** used to configure servers, deploy applications, and orchestrate multi-machine tasks — all from simple, human-readable text files.

Think of it like a recipe book for your infrastructure. Instead of manually SSHing into 50 servers and typing the same commands over and over, you write down the steps once (in a file called a **playbook**), and Ansible executes those steps on all 50 servers for you, consistently and repeatably.

**Analogy:** Imagine you're a manager with 50 employees, and every Monday you need them all to update their desk nameplates. You could walk to each desk individually and tell them what to do (manual, error-prone, slow), or you could send one email with clear instructions that everyone follows at the same time (Ansible). Ansible is that "one email" — except it also *checks* whether the nameplate already says the right thing before bothering to change it.

### Why Ansible? (The Problem It Solves)

Before tools like Ansible, system administrators managed servers in one of two ways:

| Approach | Problem |
|---|---|
| **Manual (SSH + shell commands)** | Doesn't scale past a handful of servers. Impossible to track what was changed, when, or why. Prone to "it works on this server but not that one" drift. |
| **Custom shell scripts** | Scripts aren't idempotent (running them twice can break things). No built-in inventory, no parallelism, no error handling, hard to reuse. |

Ansible solves this with three core properties:

1. **Idempotency** — Running the same playbook 100 times produces the same end result as running it once. If a package is already installed, Ansible skips reinstalling it. This makes automation *safe to re-run*.
2. **Agentless** — Unlike Puppet or Chef, Ansible doesn't require installing special software (an "agent") on every managed machine. It just needs SSH (for Linux) or WinRM (for Windows) access, and Python on the target.
3. **Declarative, human-readable syntax** — You describe the *desired state* ("this package should be installed," "this service should be running") rather than writing imperative step-by-step logic. Playbooks are written in YAML, which reads almost like plain English.

**Why does this matter to you (a Kubernetes/AWS/Terraform practitioner)?**

You already use Terraform to provision *infrastructure* (the EC2 instance, the VPC, the EKS cluster itself). Ansible fills a different but complementary gap: **configuration management** — what happens *inside* those machines after they exist. A common real-world pattern:

```
Terraform  →  provisions EC2 instances / EKS worker nodes / VPC
Ansible    →  configures OS packages, users, files, application deployment, bootstrap scripts on those instances
```

They are not competitors — they are frequently used together, each doing what it's best at.

### How Does Ansible Work? (High-Level Flow)

```
┌─────────────────────┐
│   Control Node       │   (your laptop, a CI runner, a bastion host)
│  - Ansible installed │
│  - Playbooks (YAML)  │
│  - Inventory file    │
└──────────┬───────────┘
           │  SSH (Linux) / WinRM (Windows) — no agent needed
           ▼
┌───────────────────────────────────────────────────┐
│                Managed Nodes (targets)              │
│  server1.example.com   server2.example.com  ...     │
│  (only needs Python installed — that's it)           │
└───────────────────────────────────────────────────┘
```

Step-by-step, when you run `ansible-playbook site.yml`:

1. Ansible reads the **inventory** to determine *which* machines to target.
2. It reads the **playbook** to determine *what* to do.
3. For each task, it connects to the target over SSH.
4. It copies a small Python script (a "module") to the target and executes it.
5. The module checks the *current state* of the system (e.g., "is nginx installed?").
6. If the current state already matches the desired state, Ansible reports `ok` (nothing changes — idempotency in action).
7. If not, it makes the change and reports `changed`.
8. Results are streamed back to the control node and printed to your terminal.

Crucially: **there is no persistent agent running on the managed nodes.** After the SSH session ends, nothing of Ansible remains on the target machine (aside from the effects of whatever it configured).


---

## 2. Installation

### What

Ansible needs to be installed **only on the control node** (the machine you run commands from). Managed nodes need nothing but SSH access and Python 3 — Ansible ships itself over on demand.

### Why these specific methods

`pip` (Python's package manager) is the officially recommended install method because it gets you the latest version fastest and works identically across Linux/macOS. OS package managers (`apt`, `yum`/`dnf`) are more stable/older but easier to integrate with system package management and are preferred in production/hardened environments where you don't want ad-hoc pip installs floating around.

### How

#### Option 1 — pip (recommended, cross-platform)

```bash
# Ensure Python 3 and pip are present
python3 --version
pip3 --version

# Install Ansible (installs the full ansible package, including all collections)
pip3 install --user ansible

# OR install just the minimal core (lighter weight, fewer bundled collections)
pip3 install --user ansible-core

# Verify installation
ansible --version
```

> **Note:** `ansible` (the "full" package) bundles thousands of community modules/collections. `ansible-core` is the minimal engine — you add collections as needed via `ansible-galaxy collection install`. For learning, install the full `ansible` package.

#### Option 2 — Ubuntu / Debian (APT)

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

ansible --version
```

#### Option 3 — RHEL / CentOS / Amazon Linux (DNF/YUM)

```bash
sudo dnf install -y epel-release   # RHEL/CentOS only — Amazon Linux 2023 doesn't need this
sudo dnf install -y ansible

# OR, for Amazon Linux 2 specifically:
sudo amazon-linux-extras install ansible2 -y
```

#### Option 4 — macOS (Homebrew)

```bash
brew install ansible
```

#### Option 5 — Isolated install via `pipx` (best practice for avoiding dependency conflicts)

```bash
python3 -m pip install --user pipx
pipx install --include-deps ansible
```

`pipx` installs Ansible into its own isolated virtual environment, so it won't conflict with other Python projects on your machine — this is the cleanest method if you already juggle multiple Python tool versions (which, given your Terraform/EKS tooling, you likely do).

#### Verifying installation

```bash
ansible --version
```

Expected output (versions will vary):

```
ansible [core 2.17.1]
  config file = None
  configured module search path = ['/home/user/.ansible/plugins/modules', ...]
  ansible python module location = /home/user/.local/lib/python3.11/site-packages/ansible
  ansible collection location = /home/user/.ansible/collections
  executable location = /home/user/.local/bin/ansible
  python version = 3.11.6
```

#### Target/Managed Node Requirements

Managed nodes need only:

1. **SSH server** running and reachable.
2. **Python 3** installed (Ansible auto-detects the interpreter; on very old systems you may need to set `ansible_python_interpreter` explicitly).
3. An SSH user with appropriate permissions (often paired with `sudo`/`become` for privilege escalation).

```bash
# Quick check from control node — does connectivity + Python work on the target?
ansible all -i "server1.example.com," -m ping -u ec2-user --private-key ~/.ssh/mykey.pem
```

Expected success output:

```
server1.example.com | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.9"
    },
    "changed": false,
    "ping": "pong"
}
```

> **Important distinction:** the `ping` module here is **not** an ICMP ping. It's a connectivity + Python-availability check over SSH. It confirms Ansible can log in and run modules — nothing more.


---

## 3. Core Architecture & Concepts

### What — The Building Blocks

| Term | What it is | Analogy |
|---|---|---|
| **Control Node** | The machine where Ansible is installed and from which you run commands | The "manager's office" |
| **Managed Node** | A target server Ansible configures | An "employee's desk" |
| **Inventory** | A file listing which managed nodes exist, and how they're grouped | The "employee directory" |
| **Module** | A small, reusable unit of work (e.g., install a package, copy a file, start a service) | A single "instruction card" (e.g. "install this") |
| **Task** | One call to a module, with specific parameters, inside a playbook | A filled-out instruction card ("install nginx") |
| **Playbook** | A YAML file containing an ordered list of plays (which contain tasks) | The full "recipe book" |
| **Play** | A mapping of a set of tasks to a set of hosts | One "recipe" in the book, targeted at specific "diners" (hosts) |
| **Role** | A reusable, structured bundle of tasks, templates, files, variables, and handlers | A pre-packaged "meal kit" you can reuse across recipes |
| **Handler** | A task that only runs when notified by another task (typically to restart a service after a config change) | "Only ring the bell if something actually changed" |
| **Facts** | Auto-discovered information about a managed node (OS, IP, memory, etc.) | The employee's "ID badge" info, read automatically |
| **Collection** | A distributable bundle of modules, roles, and plugins (e.g., `amazon.aws`, `community.general`) | A "toolbox" of related instruction cards |

### Why this architecture

Ansible's design separates **what to do** (playbooks) from **where to do it** (inventory) from **how it's actually done** (modules). This separation is intentional:

- You can reuse the *same* playbook across dev/staging/prod by simply pointing it at a different inventory.
- You can reuse the *same* role (e.g., "install and configure nginx") across many different playbooks/projects.
- Modules abstract away OS differences — the `package` module, for instance, calls `apt` on Ubuntu and `yum`/`dnf` on RHEL automatically, so your playbook stays OS-agnostic.

### How it fits together — a mental model

```
inventory.ini  ──┐
                  ├──►  ansible-playbook site.yml  ──►  results printed to terminal
site.yml (playbook) ┘
    │
    ├── Play 1: hosts: webservers
    │     ├── Task: install nginx     (module: ansible.builtin.package)
    │     ├── Task: copy config       (module: ansible.builtin.template)
    │     └── Handler: restart nginx  (only fires if config task reported "changed")
    │
    └── Play 2: hosts: dbservers
          └── Task: install postgresql
```

### Execution Strategy — How tasks actually run across hosts

By default, Ansible uses the `linear` strategy: **every host executes Task 1 before any host moves to Task 2.** This is a crucial detail people miss.

```
Task 1: install nginx
  ├── host1: done ✓
  ├── host2: done ✓
  └── host3: done ✓   ← Ansible waits for ALL hosts to finish Task 1
Task 2: start nginx     ← ...before ANY host starts Task 2
  ├── host1: done ✓
  └── ...
```

This matters for rolling deployments — if you want host1 to fully finish *all* tasks before host2 even starts, you'd use the `serial` keyword (covered in the Playbooks section) combined with the `free` strategy, or explicit batching.

**Forks (parallelism):** By default Ansible runs against 5 hosts simultaneously (`forks = 5` in `ansible.cfg`). If you have 50 target hosts, it processes them in batches of 5 for each task. Increase this for large fleets:

```ini
# ansible.cfg
[defaults]
forks = 20
```


---

## 4. YAML Primer

### What

YAML ("YAML Ain't Markup Language") is the data format Ansible playbooks are written in. It's whitespace-sensitive (like Python) and designed to be human-readable.

### Why YAML (and why it trips people up)

YAML was chosen because it maps naturally onto nested data structures (lists, dictionaries) without the visual noise of JSON's braces/brackets. The tradeoff: **indentation errors are the #1 cause of Ansible playbook failures for beginners.** Unlike Python, YAML doesn't require a fixed indent size — but it demands *consistency* within a block.

### How — Key Syntax Rules

```yaml
# Comments start with #

# A dictionary (key-value pairs)
name: John
age: 30

# A nested dictionary
person:
  name: John
  age: 30

# A list
fruits:
  - apple
  - banana
  - cherry

# A list of dictionaries (very common in playbooks — this is how "tasks" are structured)
users:
  - name: alice
    role: admin
  - name: bob
    role: viewer

# Strings usually don't need quotes, but quote when values contain
# special characters, start with a number, or could be misread as booleans
description: "Deploys version 2.0"
port: "8080"          # quoted because it's used as a string, not integer
enabled: true          # boolean — no quotes
raw_string: 'Don''t use unquoted colons: like this'

# Multi-line strings
short_desc: >
  This folds into
  a single line with spaces.

exact_format: |
  This preserves
  line breaks
  exactly as written.
```

**Critical gotcha table:**

| Mistake | Why it breaks |
|---|---|
| Mixing tabs and spaces | YAML forbids tabs for indentation — always use spaces |
| Inconsistent indent within a block | Every item at the same "level" must have identical indentation |
| Forgetting the space after `:` | `key:value` is invalid; must be `key: value` |
| Unquoted strings starting with special chars (`{`, `[`, `*`, `&`, `!`, `%`) | YAML tries to interpret these as its own syntax |
| Using `yes`/`no`/`on`/`off` unquoted expecting a string | YAML 1.1 treats these as booleans |

**Validate YAML before running a playbook:**

```bash
# Quick syntax check without executing anything
ansible-playbook site.yml --syntax-check

# Or use yamllint for style/lint issues
pip3 install yamllint
yamllint site.yml
```


---

## 5. Inventory

### What

The inventory is the list of managed nodes Ansible knows about, optionally organized into groups. It can be a **static file** (INI or YAML format) or **generated dynamically** (e.g., pulled live from AWS EC2 tags — covered in Section 17).

### Why grouping matters

Real infrastructure isn't one flat list of servers — you have webservers, dbservers, servers in different regions, different environments (dev/staging/prod). Groups let a single playbook target exactly the right subset, and let you define variables that apply only to specific groups (e.g., all `dbservers` get a `db_port: 5432` variable automatically).

### How — Static Inventory (INI format)

```ini
# inventory.ini

[webservers]
web1.example.com
web2.example.com ansible_host=10.0.1.15

[dbservers]
db1.example.com

# A "group of groups" — combine webservers + dbservers into one "production" group
[production:children]
webservers
dbservers

# Group-level variables (applies to every host in [webservers])
[webservers:vars]
http_port=80
env=production

# A range shorthand — expands to web01..web10
[webservers]
web[01:10].example.com
```

### How — Static Inventory (YAML format — preferred for complex setups)

```yaml
# inventory.yml
all:
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_host: 10.0.1.15
      vars:
        http_port: 80
        env: production
    dbservers:
      hosts:
        db1.example.com:
      vars:
        db_port: 5432
  vars:
    ansible_user: ec2-user
    ansible_ssh_private_key_file: ~/.ssh/prod-key.pem
```

### Special / Built-in Groups

| Group | Meaning |
|---|---|
| `all` | Every host in the inventory, implicitly |
| `ungrouped` | Any host not assigned to a user-defined group |

### Common `ansible_*` Connection Variables

| Variable | Purpose |
|---|---|
| `ansible_host` | The actual IP/hostname to connect to (if different from the inventory alias) |
| `ansible_port` | SSH port (default 22) |
| `ansible_user` | SSH username |
| `ansible_ssh_private_key_file` | Path to the SSH private key |
| `ansible_connection` | Connection type: `ssh` (default), `local`, `winrm`, `docker` |
| `ansible_python_interpreter` | Explicit path to Python on the target (needed for some minimal OS images) |
| `ansible_become` | Whether to escalate privileges (`sudo`) for tasks — `true`/`false` |
| `ansible_become_method` | Escalation method: `sudo`, `su`, etc. |

### Verifying and Inspecting Inventory

```bash
# List all hosts Ansible sees
ansible-inventory -i inventory.ini --list

# Pretty-printed group/host tree
ansible-inventory -i inventory.ini --graph

# Ping every host in the "webservers" group
ansible webservers -i inventory.ini -m ping
```

Example `--graph` output:

```
@all:
  |--@production:
  |  |--@webservers:
  |  |  |--web1.example.com
  |  |  |--web2.example.com
  |  |--@dbservers:
  |  |  |--db1.example.com
  |--@ungrouped:
```


---

## 6. Ad-Hoc Commands

### What

Ad-hoc commands are one-off, single-task Ansible runs executed directly from the command line — no playbook file needed. Think of them as the "quick shell command" equivalent.

### Why use them

Not every task deserves a full playbook. If you just want to check disk space across 30 servers, or restart a service once, an ad-hoc command is faster than writing and saving a YAML file. They're also invaluable for debugging and exploration.

### How — Syntax

```bash
ansible <host-pattern> -i <inventory> -m <module> -a "<module arguments>" [options]
```

### Examples

```bash
# Connectivity check
ansible all -i inventory.ini -m ping

# Run a raw shell command on all webservers
ansible webservers -i inventory.ini -m shell -a "df -h"

# Install a package (idempotent — won't reinstall if already present)
ansible webservers -i inventory.ini -m ansible.builtin.yum -a "name=httpd state=present" --become

# Copy a file to all hosts
ansible all -i inventory.ini -m copy -a "src=./app.conf dest=/etc/app/app.conf" --become

# Restart a service
ansible dbservers -i inventory.ini -m service -a "name=postgresql state=restarted" --become

# Create a user
ansible all -i inventory.ini -m user -a "name=deploy state=present shell=/bin/bash" --become

# Gather and display facts about a host (useful for debugging conditionals/templates)
ansible web1.example.com -i inventory.ini -m setup

# Limit to a single host from a larger group
ansible webservers -i inventory.ini -m ping --limit web1.example.com

# Run with 10 parallel forks instead of the default 5
ansible all -i inventory.ini -m ping -f 10
```

### `command` vs `shell` module — an important distinction

| Module | Behavior |
|---|---|
| `command` (default if you omit `-m`) | Runs the command directly, **without** invoking a shell. No pipes (`\|`), redirects (`>`), or env variable expansion (`$HOME`). Safer, preferred default. |
| `shell` | Runs through `/bin/sh`, so pipes/redirects/variables work — but it's less predictable and slightly less secure (shell injection risk if arguments include untrusted input). |

```bash
# This FAILS silently or errors — command module can't handle pipes
ansible all -m command -a "ps aux | grep nginx"

# This WORKS — shell module invokes an actual shell
ansible all -m shell -a "ps aux | grep nginx"
```

**Rule of thumb:** default to `command` (or better, a purpose-built module like `package`, `service`, `copy`) and only reach for `shell` when you genuinely need shell features.


---

## 7. Playbooks

### What

A playbook is a YAML file that defines one or more **plays**. Each play maps a group of hosts to an ordered list of **tasks**. This is the primary way Ansible automation is written and stored for reuse (as opposed to throwaway ad-hoc commands).

### Why playbooks over ad-hoc commands

Playbooks are version-controllable, reviewable (via pull requests — fits your GitHub-repo workflow), composable (via roles/includes), and support advanced features ad-hoc commands can't: handlers, conditionals, loops, error handling, variable files, tags, and multi-play orchestration across different host groups in a single run.

### How — Anatomy of a Playbook

```yaml
---
# site.yml
- name: Configure web servers                # Play 1
  hosts: webservers                           # Target group from inventory
  become: true                                # Escalate privileges (sudo) for all tasks in this play
  vars:
    http_port: 8080
    app_version: "2.3.1"

  tasks:
    - name: Install nginx
      ansible.builtin.package:
        name: nginx
        state: present

    - name: Copy nginx configuration
      ansible.builtin.template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        owner: root
        group: root
        mode: '0644'
      notify: Restart nginx                   # Triggers the handler below, only if this task reports "changed"

    - name: Ensure nginx is running and enabled on boot
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted

- name: Configure database servers            # Play 2 — different hosts, different tasks
  hosts: dbservers
  become: true
  tasks:
    - name: Install PostgreSQL
      ansible.builtin.package:
        name: postgresql-server
        state: present
```

### Running a Playbook

```bash
# Basic run
ansible-playbook -i inventory.ini site.yml

# Dry run — show what WOULD change, without actually changing anything
ansible-playbook -i inventory.ini site.yml --check

# Dry run + show line-level diffs of file changes
ansible-playbook -i inventory.ini site.yml --check --diff

# Limit execution to a subset of hosts
ansible-playbook -i inventory.ini site.yml --limit web1.example.com

# Pass/override variables from the command line
ansible-playbook -i inventory.ini site.yml -e "app_version=2.4.0"

# Start execution from a specific task (useful when debugging a failed run)
ansible-playbook -i inventory.ini site.yml --start-at-task="Copy nginx configuration"

# Increase verbosity for debugging (up to -vvvv)
ansible-playbook -i inventory.ini site.yml -vvv

# Ask for the sudo password interactively instead of using keys/NOPASSWD
ansible-playbook -i inventory.ini site.yml --ask-become-pass
```

### Reading Playbook Output

```
PLAY [Configure web servers] **************************************************

TASK [Gathering Facts] ********************************************************
ok: [web1.example.com]

TASK [Install nginx] **********************************************************
changed: [web1.example.com]

TASK [Copy nginx configuration] ***********************************************
changed: [web1.example.com]

TASK [Ensure nginx is running and enabled on boot] ****************************
ok: [web1.example.com]

RUNNING HANDLER [Restart nginx] ***********************************************
changed: [web1.example.com]

PLAY RECAP *********************************************************************
web1.example.com : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

| Status color/word | Meaning |
|---|---|
| `ok` (green) | Task ran, nothing needed to change — desired state already matched |
| `changed` (yellow) | Task ran and made a change to reach desired state |
| `failed` (red) | Task errored — by default, that host is removed from the rest of the play |
| `skipped` (cyan) | Task's `when` condition evaluated false, so it didn't run |
| `unreachable` (red) | Ansible couldn't connect to the host at all (SSH/network issue) |

### Rolling Deployments with `serial`

```yaml
- name: Rolling deploy across the fleet
  hosts: webservers
  serial: 2          # Only touch 2 hosts at a time, complete all tasks, then move to next batch
  # Also supports percentages: serial: "25%"
  # Or a progressive list: serial: [1, 5, "100%"]  (canary, then wider batches)
  tasks:
    - name: Deploy new app version
      ansible.builtin.git:
        repo: https://github.com/example/app.git
        dest: /opt/app
        version: "{{ app_version }}"
      notify: Restart app service
```

This is the Ansible equivalent of a Kubernetes rolling update — it lets you deploy to a subset of servers, verify health, then proceed, rather than taking your entire fleet down simultaneously.


---

## 8. Variables, Facts & Precedence

### What

Variables let playbooks be dynamic and reusable rather than hardcoded. **Facts** are a special category of variables — automatically discovered by Ansible about each host (OS type, IP addresses, CPU count, memory, etc.), gathered at the start of every play via the implicit `Gathering Facts` task.

### Why precedence matters (and why this is a common source of confusion)

Variables can be defined in **many different places** simultaneously — inventory, playbook, role defaults, command line, facts. When the same variable name is defined in more than one place, Ansible needs a deterministic rule for which value "wins." Understanding this precedence order is essential for debugging "why isn't my variable taking effect?" issues.

### How — Where Variables Come From

```yaml
# 1. Role defaults (lowest precedence — easily overridden)
# roles/myrole/defaults/main.yml
http_port: 80

# 2. Inventory variables
# inventory.yml
webservers:
  vars:
    http_port: 8080

# 3. Playbook 'vars:' block
- hosts: webservers
  vars:
    http_port: 8888

# 4. Task-level vars
  tasks:
    - name: Show port
      debug:
        msg: "{{ http_port }}"
      vars:
        http_port: 9999

# 5. Extra vars via command line (HIGHEST precedence — always wins)
# ansible-playbook site.yml -e "http_port=7777"
```

### Ansible Variable Precedence (lowest → highest, abbreviated official order)

1. Role defaults (`roles/*/defaults/main.yml`)
2. Inventory file/group/host vars
3. Playbook group_vars / host_vars
4. Playbook `vars:`
5. Role `vars/main.yml`
6. Block/task `vars:`
7. Registered variables (`register:`) / facts
8. Extra vars (`-e` on the command line) — **always wins, no exceptions**

> **Practical takeaway:** if you're debugging "why won't my variable change," check whether someone is passing `-e` on the command line — it silently overrides everything else, which is by design (used for CI/CD pipelines to inject environment-specific values).

### Facts — Auto-Discovered Variables

```bash
# See every fact Ansible knows about a host
ansible web1.example.com -i inventory.ini -m setup
```

Sample (truncated) output:

```json
{
    "ansible_facts": {
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_version": "22.04",
        "ansible_default_ipv4": {
            "address": "10.0.1.15"
        },
        "ansible_processor_vcpus": 2,
        "ansible_memtotal_mb": 3936,
        "ansible_hostname": "web1"
    }
}
```

Using facts inside a playbook:

```yaml
- name: Show OS-specific info
  debug:
    msg: "This host runs {{ ansible_distribution }} {{ ansible_distribution_version }}"

- name: Install package only on Debian-family systems
  ansible.builtin.apt:
    name: nginx
    state: present
  when: ansible_facts['os_family'] == "Debian"
```

**Performance tip:** fact-gathering (SSH + running a discovery script) adds latency to every play. If you don't need facts, disable it:

```yaml
- hosts: webservers
  gather_facts: false
```

### Registering Task Output as a Variable

```yaml
- name: Check if a file exists
  ansible.builtin.stat:
    path: /etc/app/config.yml
  register: config_file

- name: Only run this if the file doesn't exist
  ansible.builtin.debug:
    msg: "Config file is missing!"
  when: not config_file.stat.exists
```

`register` captures a task's full result object (return code, stdout, stderr, changed status, etc.) into a variable you can reference in later tasks — this is the primary mechanism for making tasks conditional on the outcome of previous tasks.


---

## 9. Conditionals & Loops

### What

Conditionals (`when`) let tasks run only under certain circumstances. Loops (`loop`, `with_items`, etc.) let a single task run repeatedly against a list of items instead of writing the same task multiple times.

### Why

Real infrastructure isn't uniform — you often need "install this package only on Ubuntu" or "create these 5 users" without duplicating YAML five times. Conditionals and loops keep playbooks DRY (Don't Repeat Yourself) and adaptable across heterogeneous environments.

### How — Conditionals

```yaml
- name: Install nginx on Debian-based systems
  ansible.builtin.apt:
    name: nginx
    state: present
  when: ansible_facts['os_family'] == "Debian"

- name: Install nginx on RedHat-based systems
  ansible.builtin.yum:
    name: nginx
    state: present
  when: ansible_facts['os_family'] == "RedHat"

# Multiple conditions — AND (all must be true, using a list)
- name: Restart only if changed AND in production
  ansible.builtin.service:
    name: nginx
    state: restarted
  when:
    - config_result.changed
    - env == "production"

# OR condition
- name: Run on either Ubuntu or Debian
  debug:
    msg: "Debian-family OS detected"
  when: ansible_distribution == "Ubuntu" or ansible_distribution == "Debian"

# Checking if a variable is even defined (avoids errors on undefined vars)
- name: Only run if custom_var was set
  debug:
    msg: "{{ custom_var }}"
  when: custom_var is defined
```

### How — Loops

```yaml
# Simple loop over a list
- name: Create multiple users
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
  loop:
    - alice
    - bob
    - charlie

# Loop over a list of dictionaries — very common real-world pattern
- name: Create users with specific roles
  ansible.builtin.user:
    name: "{{ item.name }}"
    groups: "{{ item.group }}"
    state: present
  loop:
    - { name: alice, group: admin }
    - { name: bob, group: developers }
    - { name: charlie, group: viewers }

# Loop over a variable defined elsewhere
- name: Install a list of packages
  ansible.builtin.package:
    name: "{{ item }}"
    state: present
  loop: "{{ required_packages }}"
  # where required_packages is defined in vars as:
  # required_packages: [git, curl, htop, vim]

# Looping with an index
- name: Show index and value
  debug:
    msg: "Item {{ index }}: {{ item }}"
  loop: "{{ ['a', 'b', 'c'] }}"
  loop_control:
    index_var: index

# Retry a task until a condition succeeds (polling pattern)
- name: Wait for application to become healthy
  ansible.builtin.uri:
    url: "http://localhost:8080/health"
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 10
  delay: 5     # seconds between retries
```

> **Note on legacy syntax:** older Ansible content uses `with_items`, `with_dict`, `with_fileglob`, etc. These still work but `loop` (introduced in Ansible 2.5) is the modern, recommended replacement for most cases — it's simpler and more predictable. You'll still see `with_*` frequently in older codebases/roles from Galaxy.


---

## 10. Handlers & Notifications

### What

A handler is a special kind of task that only executes when explicitly **notified** by another task — and only if that task reported `changed`. The most common use case: restart a service *only* after its configuration file actually changed.

### Why

Without handlers, you'd either (a) restart services on *every* playbook run regardless of whether anything changed (wasteful, causes unnecessary downtime/blips), or (b) forget to restart them when config does change (stale config bugs). Handlers solve both problems — they're event-driven, not unconditional.

### How

```yaml
- hosts: webservers
  become: true
  tasks:
    - name: Copy nginx config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify: Restart nginx        # Only queues the handler if this task changes something

    - name: Copy app config
      ansible.builtin.template:
        src: app.conf.j2
        dest: /etc/app/app.conf
      notify: Restart nginx        # Multiple tasks can notify the SAME handler

  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

### Key behaviors to understand

1. **Handlers run once, even if notified multiple times.** If 5 tasks in a play all notify "Restart nginx," it still only restarts once — at the end.
2. **Handlers run at the END of the play by default** — not immediately when notified. All tasks in the play complete first, then all queued handlers fire in the order they're *defined* (not the order they were notified).
3. **To force a handler to run immediately** (mid-play), use `meta: flush_handlers`:

```yaml
tasks:
  - name: Update config
    template:
      src: app.conf.j2
      dest: /etc/app.conf
    notify: Restart app

  - name: Force handlers to run now
    meta: flush_handlers

  - name: This task now sees the app already restarted
    uri:
      url: http://localhost:8080/health
```

4. **Handlers can notify other handlers** (chains), and can also use `listen` to group multiple handler names under one notification topic:

```yaml
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
    listen: "restart web stack"

  - name: Restart php-fpm
    service:
      name: php-fpm
      state: restarted
    listen: "restart web stack"

tasks:
  - name: Update shared config
    template:
      src: shared.conf.j2
      dest: /etc/shared.conf
    notify: "restart web stack"    # Fires BOTH handlers above
```


---

## 11. Templates (Jinja2)

### What

Templates are files with embedded variables/logic (using **Jinja2** templating syntax) that Ansible renders into final, static config files on the target host — via the `template` module. This is how you generate config files that differ per-host or per-environment from a single source file.

### Why

Hardcoding config files means maintaining N nearly-identical copies for N environments. Templates let you maintain **one** source file with placeholders, and Ansible fills in the blanks differently for each host based on that host's variables/facts.

### How

**Source template file** (`templates/nginx.conf.j2` — the `.j2` extension is convention, not required):

```jinja2
server {
    listen {{ http_port }};
    server_name {{ ansible_fqdn }};

    root /var/www/{{ app_name }};

    {% if enable_ssl %}
    listen 443 ssl;
    ssl_certificate     /etc/ssl/certs/{{ app_name }}.crt;
    ssl_certificate_key /etc/ssl/private/{{ app_name }}.key;
    {% endif %}

    location / {
        proxy_pass http://127.0.0.1:{{ backend_port }};
    }

    # Loop over a list variable to generate repeated blocks
    {% for allowed_ip in allowed_ips %}
    allow {{ allowed_ip }};
    {% endfor %}
    deny all;
}

# Generated by Ansible on {{ ansible_date_time.date }} — DO NOT EDIT MANUALLY
```

**The task that renders it:**

```yaml
- name: Deploy nginx config from template
  ansible.builtin.template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}.conf
    owner: root
    group: root
    mode: '0644'
    validate: 'nginx -t -c %s'   # Runs this validation command against a TEMP copy before overwriting the real file — prevents deploying broken configs
  notify: Restart nginx
```

### Common Jinja2 Filters

Filters transform a variable's value inline — syntax is `{{ variable | filter_name }}`.

```jinja2
{{ app_name | upper }}                     # UPPERCASE
{{ app_name | lower }}                     # lowercase
{{ my_list | length }}                     # count of items
{{ my_list | join(', ') }}                 # "a, b, c"
{{ undefined_var | default('fallback') }}  # use 'fallback' if undefined
{{ password | password_hash('sha512') }}   # hash a password
{{ some_dict | to_json }}                  # serialize to JSON
{{ my_string | regex_replace('foo', 'bar') }}
{{ my_list | unique }}
{{ my_list | sort }}
{{ file_content | b64encode }}
```

### `template` vs `copy` — when to use which

| Module | Use when |
|---|---|
| `ansible.builtin.copy` | The file content is **static** — identical on every target, no variable substitution needed |
| `ansible.builtin.template` | The file content **needs variable/fact substitution** (Jinja2 processing) before being placed on the target |


---

## 12. Roles

### What

A role is a **standardized directory structure** that bundles related tasks, handlers, templates, files, variables, and default values into a self-contained, reusable unit. Think of a role as a "package" for a specific piece of functionality (e.g., "install and configure nginx," "harden SSH," "deploy my-app").

### Why

As playbooks grow, cramming everything into one giant YAML file becomes unmanageable. Roles let you:

- **Reuse** the same automation across many projects/playbooks (e.g., an "nginx" role used by 10 different apps).
- **Share** publicly via Ansible Galaxy (like npm packages or Terraform modules — this parallel should feel familiar).
- **Organize** logically so new team members can navigate by convention, not guesswork.

### How — Standard Role Directory Structure

```
roles/
└── nginx/
    ├── defaults/
    │   └── main.yml       # Default variable values (LOWEST precedence — easily overridden)
    ├── vars/
    │   └── main.yml       # "Fixed" variables for this role (higher precedence than defaults)
    ├── tasks/
    │   └── main.yml       # The core list of tasks — entry point for the role
    ├── handlers/
    │   └── main.yml       # Handlers, e.g. "restart nginx"
    ├── templates/
    │   └── nginx.conf.j2  # Jinja2 templates used by this role's tasks
    ├── files/
    │   └── static.conf    # Static files copied as-is
    ├── meta/
    │   └── main.yml       # Role metadata + dependencies on other roles
    └── README.md          # Documentation for the role
```

### Example: A Minimal `nginx` Role

```yaml
# roles/nginx/defaults/main.yml
http_port: 80
app_name: default-app
```

```yaml
# roles/nginx/tasks/main.yml
---
- name: Install nginx
  ansible.builtin.package:
    name: nginx
    state: present

- name: Deploy config
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/{{ app_name }}.conf
  notify: Restart nginx

- name: Ensure nginx running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
```

```yaml
# roles/nginx/handlers/main.yml
---
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
```

### Using a Role in a Playbook

```yaml
# site.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  roles:
    - nginx                         # Simplest form — uses role defaults

    - role: nginx                   # Or pass role-specific variables inline
      vars:
        http_port: 8080
        app_name: my-production-app
```

Modern alternative syntax using `include_role` / `import_role` (allows roles mid-task-list, conditionally, or in loops):

```yaml
tasks:
  - name: Apply nginx role only on webservers group
    ansible.builtin.include_role:
      name: nginx
    when: "'webservers' in group_names"
```

### `import_role`/`import_tasks` vs `include_role`/`include_tasks`

| | Static (`import_*`) | Dynamic (`include_*`) |
|---|---|---|
| **When processed** | At playbook *parse* time (before execution starts) | At *runtime*, as the play executes |
| **Supports `loop`** | No | Yes |
| **Supports host-variable-based conditionals reliably** | Less flexible | Yes — can use `when` based on facts gathered during the run |
| **Performance** | Slightly faster (pre-resolved) | Slightly slower (resolved per-host, per-run) |
| **Use when** | Structure is fixed and known ahead of time | You need conditional/looped role inclusion |

### Scaffolding a New Role

```bash
ansible-galaxy init roles/my-new-role
```

This auto-generates the full standard directory structure shown above — saves you from typing it by hand.


---

## 13. Ansible Galaxy & Collections

### What

**Ansible Galaxy** (`galaxy.ansible.com`) is the public registry for sharing and downloading Ansible **roles** and **collections** — conceptually similar to the Terraform Registry or Docker Hub, but for Ansible content. A **Collection** is the modern packaging format bundling modules, plugins, roles, and playbooks together (e.g., `amazon.aws`, `community.general`, `kubernetes.core`).

### Why

You rarely need to write automation for common tasks (like managing AWS resources, Kubernetes objects, or MySQL databases) from scratch — the community (and vendors like AWS, Red Hat, and Microsoft) publish maintained, tested collections. Since Ansible 2.10, most modules beyond a small "builtin" core were split out of the main package into separately-versioned collections — this is why you'll see module names like `amazon.aws.ec2_instance` instead of a bare `ec2_instance`.

### How

```bash
# Install a collection (this is what gives you AWS modules, e.g. amazon.aws.ec2_instance)
ansible-galaxy collection install amazon.aws

# Install a specific version
ansible-galaxy collection install amazon.aws:==7.1.0

# Install a role from Galaxy
ansible-galaxy role install geerlingguy.nginx

# List installed collections
ansible-galaxy collection list

# Search is done via the web UI at galaxy.ansible.com, or:
ansible-galaxy search nginx --platforms EL
```

### `requirements.yml` — Declaring Dependencies (like `requirements.txt` for Python, or a Terraform `required_providers` block)

```yaml
# requirements.yml
collections:
  - name: amazon.aws
    version: ">=7.0.0"
  - name: kubernetes.core
    version: "3.0.1"
  - name: community.general

roles:
  - name: geerlingguy.nginx
    version: "3.1.4"
```

```bash
# Install everything declared in requirements.yml — this is the reproducible, CI-friendly pattern
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

> **Best practice:** always commit a `requirements.yml` to your repo and pin versions. Without it, a fresh clone of your repo won't know which collections to install, and playbooks referencing `amazon.aws.ec2_instance` will fail with "module not found."

### Namespacing — Why Modules Look Like `amazon.aws.ec2_instance`

Format: `<namespace>.<collection_name>.<module_name>`

| Example | Meaning |
|---|---|
| `ansible.builtin.copy` | Ships with Ansible core, always available |
| `amazon.aws.ec2_instance` | From the AWS collection maintained by the Ansible/AWS community |
| `kubernetes.core.k8s` | From the Kubernetes collection — lets Ansible apply/manage K8s manifests |
| `community.general.docker_container` | From the large "community.general" grab-bag collection |


---

## 14. Ansible Vault (Secrets Management)

### What

Ansible Vault is a built-in feature that **encrypts sensitive data** (passwords, API keys, private keys, entire files) so they can be safely committed to version control (like your GitHub repo) without exposing plaintext secrets.

### Why

Playbooks frequently need secrets — a database password, an AWS access key, a TLS private key. Committing these in plaintext to Git is a critical security failure (git history is forever, and repos leak). Vault solves this by encrypting the values/files at rest; they're only decrypted in-memory at the moment Ansible actually needs them during a run, using a password/key you supply separately (never committed alongside the encrypted content).

**How this compares to what you already know:** this solves the same problem as HashiCorp Vault or `sops` for Terraform — "how do I keep secrets out of my Git history while still using them in automation." Ansible Vault is the built-in, lower-ceremony version of that idea (no external service required, unlike HashiCorp Vault).

### How

#### Encrypting an entire file

```bash
# Create a new encrypted file interactively
ansible-vault create secrets.yml
# Opens your $EDITOR — whatever you type gets saved encrypted

# Encrypt an EXISTING plaintext file
ansible-vault encrypt vars/prod-secrets.yml

# View decrypted contents without permanently decrypting the file on disk
ansible-vault view secrets.yml

# Edit an already-encrypted file (decrypts, opens editor, re-encrypts on save)
ansible-vault edit secrets.yml

# Permanently decrypt a file (rarely what you want — removes encryption)
ansible-vault decrypt secrets.yml

# Change the vault password
ansible-vault rekey secrets.yml
```

Example encrypted file content (`secrets.yml`) when viewed raw — this IS what's safe to commit to Git:

```
$ANSIBLE_VAULT;1.1;AES256
66386439653236336462626566653063336164663966303231363934653561363964363065
3162386435376439336639323235353933366131396264610a373530393563643538666331
...
```

Its decrypted contents (only visible via `ansible-vault view` or at runtime):

```yaml
db_password: "S3cur3P@ss!"
aws_secret_access_key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

#### Encrypting a single variable inline (mix plaintext and secrets in the same file)

```bash
ansible-vault encrypt_string 'S3cur3P@ss!' --name 'db_password'
```

Output — paste this directly into a normal (unencrypted) vars file:

```yaml
db_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          383635396239...
```

This is the recommended pattern for most real projects: keep `vars/main.yml` in plaintext for readability/diffing, but individual sensitive values within it are Vault-encrypted strings.

#### Running Playbooks that Use Vault-Encrypted Content

```bash
# Prompt for the vault password interactively at runtime
ansible-playbook site.yml --ask-vault-pass

# Read the vault password from a file (NEVER commit this file to Git — add to .gitignore)
ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt

# Use an executable script that RETRIEVES the password (e.g., from AWS Secrets Manager) — best practice for CI/CD
ansible-playbook site.yml --vault-password-file get_vault_pass.sh
```

#### Multiple Vault IDs (separate passwords per environment)

```bash
# Encrypt with a labeled vault ID
ansible-vault encrypt vars/prod-secrets.yml --vault-id prod@prompt
ansible-vault encrypt vars/dev-secrets.yml --vault-id dev@prompt

# Run referencing multiple vault IDs — each decrypted with its own password
ansible-playbook site.yml \
  --vault-id prod@~/.vault_pass_prod.txt \
  --vault-id dev@~/.vault_pass_dev.txt
```

This lets different team members/systems hold only the passwords for the environments they're authorized to touch (e.g., CI/CD has the prod password; a junior dev only has the dev password).

### Vault Best Practices

- **Never commit the vault password itself** to Git — store it in a password manager, or better, in AWS Secrets Manager / SSM Parameter Store, fetched dynamically by a `--vault-password-file` script.
- Add `*.vault_pass*` and any plaintext password files to `.gitignore`.
- Prefer `encrypt_string` for individual secrets over encrypting entire files — this keeps your Git diffs readable (you can see *which* variable changed, structurally, even though its value is encrypted).
- In CI/CD (covered in Section 20), store the vault password as a masked/protected pipeline secret (e.g., a GitHub Actions secret), and pass it via `--vault-password-file <(echo "$VAULT_PASSWORD")`.


---

## 15. Error Handling & Blocks

### What

By default, if a task fails on a host, Ansible immediately stops running further tasks *on that host* (other hosts continue unaffected). **Blocks** group related tasks together and support `rescue` (like a `try/catch`) and `always` (like `finally`) sections for structured error handling.

### Why

Real automation needs graceful failure handling — e.g., "try to deploy the new version; if it fails, roll back to the previous version; either way, send a notification." Without blocks, you'd need fragile chains of `register` + `when` checks. Blocks give you proper exception-handling semantics.

### How — Basic Failure Control

```yaml
- name: This task might fail, but don't stop the whole play
  ansible.builtin.command: /opt/scripts/risky-operation.sh
  ignore_errors: true

- name: Fail the play manually based on custom logic
  ansible.builtin.fail:
    msg: "Disk usage is critically high!"
  when: disk_usage_percent > 90

- name: Only mark as 'changed' under specific conditions (override auto-detection)
  ansible.builtin.command: /opt/scripts/idempotent-check.sh
  register: result
  changed_when: "'MODIFIED' in result.stdout"

- name: Treat this specific 'failure' as success (e.g., exit code 2 means 'no updates needed')
  ansible.builtin.command: /usr/bin/yum check-update
  register: result
  failed_when: result.rc not in [0, 100]
```

### How — Blocks (try / rescue / always)

```yaml
tasks:
  - name: Deploy new application version
    block:
      - name: Stop the application
        ansible.builtin.service:
          name: myapp
          state: stopped

      - name: Deploy new code
        ansible.builtin.git:
          repo: https://github.com/example/app.git
          dest: /opt/app
          version: "{{ app_version }}"

      - name: Start the application
        ansible.builtin.service:
          name: myapp
          state: started

      - name: Verify health check passes
        ansible.builtin.uri:
          url: http://localhost:8080/health
          status_code: 200

    rescue:                                          # Runs ONLY if any task in "block" failed
      - name: Roll back to previous version
        ansible.builtin.git:
          repo: https://github.com/example/app.git
          dest: /opt/app
          version: "{{ previous_stable_version }}"

      - name: Restart with rolled-back version
        ansible.builtin.service:
          name: myapp
          state: restarted

      - name: Alert the team about the failed deployment
        ansible.builtin.uri:
          url: "{{ slack_webhook_url }}"
          method: POST
          body_format: json
          body:
            text: "Deployment of {{ app_version }} FAILED and was rolled back on {{ inventory_hostname }}"

    always:                                            # Runs REGARDLESS of success or failure
      - name: Log deployment attempt
        ansible.builtin.lineinfile:
          path: /var/log/deployments.log
          line: "{{ ansible_date_time.iso8601 }} - Deploy attempt for {{ app_version }} on {{ inventory_hostname }}"
```

**Execution logic:**

```
block:  runs task-by-task
   │
   ├── all succeed ──────────────► always: runs ──► play continues
   │
   └── any task fails ──► rescue: runs ──► always: runs ──► play continues (rescue "caught" the error)
```

If a task inside `rescue` *also* fails, the host is then marked failed for real, and normal failure behavior (stop tasks on that host) resumes.

### Controlling Which Hosts Halt the Play

```yaml
- hosts: webservers
  # By default, if ANY host fails a task, that host stops — but OTHER hosts continue.
  # To stop the ENTIRE play across all hosts as soon as any single host fails:
  any_errors_fatal: true

  # To require a minimum percentage of hosts to succeed before continuing:
  max_fail_percentage: 30
```


---

## 16. Tags

### What

Tags let you label individual tasks, blocks, roles, or entire plays, so you can selectively run (or skip) subsets of a playbook without executing the whole thing.

### Why

A large playbook might set up users, install packages, configure firewalls, and deploy an app — but sometimes you only want to re-run the "deploy app" part without touching everything else. Tags give you that surgical control, saving time and avoiding unnecessary changes/restarts on unrelated components.

### How

```yaml
tasks:
  - name: Install base packages
    ansible.builtin.package:
      name: "{{ item }}"
      state: present
    loop: [git, curl, vim]
    tags:
      - setup
      - packages

  - name: Configure firewall rules
    ansible.builtin.ufw:
      rule: allow
      port: "{{ item }}"
    loop: [80, 443]
    tags:
      - firewall
      - security

  - name: Deploy application code
    ansible.builtin.git:
      repo: https://github.com/example/app.git
      dest: /opt/app
    tags:
      - deploy
```

```bash
# Run ONLY tasks tagged "deploy"
ansible-playbook site.yml --tags deploy

# Run tasks tagged EITHER "deploy" OR "firewall"
ansible-playbook site.yml --tags "deploy,firewall"

# Run everything EXCEPT tasks tagged "firewall"
ansible-playbook site.yml --skip-tags firewall

# List all tags available in a playbook without running anything
ansible-playbook site.yml --list-tags
```

### Special Reserved Tags

| Tag | Behavior |
|---|---|
| `always` | Task runs every time, regardless of `--tags`/`--skip-tags` filtering (unless explicitly skipped) |
| `never` | Task is skipped by default unless explicitly requested with `--tags never` |

```yaml
- name: This always runs (e.g., critical fact-gathering)
  ansible.builtin.debug:
    msg: "Starting deployment..."
  tags:
    - always

- name: This is a dangerous, rarely-needed task
  ansible.builtin.command: /opt/scripts/wipe-database.sh
  tags:
    - never
    - dangerous
```


---

## 17. Dynamic Inventory (AWS Example)

### What

Instead of manually maintaining a static list of EC2 IP addresses (which change as instances are created/terminated/autoscaled), **dynamic inventory** queries AWS's API live, every time you run Ansible, to build the host list automatically based on filters/tags.

### Why

Static inventory files go stale immediately in cloud environments — especially if you're using Auto Scaling Groups, Karpenter-managed nodes, or any EC2 fleet with elastic capacity (all things you're already working with in EKS). Dynamic inventory means Ansible always targets whatever instances *actually exist right now*, grouped automatically by tags, region, VPC, or instance type — no manual file maintenance.

### How

#### Step 1 — Install the AWS collection

```bash
ansible-galaxy collection install amazon.aws
pip3 install boto3 botocore    # Python AWS SDK — required by the AWS collection
```

#### Step 2 — Configure AWS Credentials

Ansible's AWS collection uses the same credential chain as the AWS CLI/boto3 — so if you already have `aws configure` set up or use an instance profile/IAM role, it just works:

```bash
aws configure       # OR export AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN
```

#### Step 3 — Define the Dynamic Inventory Source

```yaml
# aws_ec2.yml  (filename MUST end in aws_ec2.yml or aws_ec2.yaml for auto-detection)
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2

# Only include running instances
filters:
  instance-state-name: running
  "tag:Environment": production

# Automatically create inventory GROUPS based on tags/attributes
keyed_groups:
  - key: tags.Role                          # e.g. tag "Role=webserver" → group [tag_Role_webserver]
    prefix: tag_Role
  - key: instance_type
    prefix: instance_type
  - key: placement.region
    prefix: aws_region

# Define what value to use as the "ansible_host" (connection address)
compose:
  ansible_host: public_ip_address

# Cache results to avoid hitting the AWS API on every single run (optional but recommended)
cache: true
cache_plugin: jsonfile
cache_connection: /tmp/ansible_inventory_cache
cache_timeout: 300
```

#### Step 4 — Verify and Use It

```bash
# View the dynamically-generated inventory
ansible-inventory -i aws_ec2.yml --graph

# Run a playbook against dynamically-discovered hosts
ansible-playbook -i aws_ec2.yml site.yml

# Target only instances in the auto-generated "webserver" group
ansible tag_Role_webserver -i aws_ec2.yml -m ping
```

Example `--graph` output:

```
@all:
  |--@aws_region_us_east_1:
  |  |--i-0abcd1234efgh5678
  |  |--i-0ijkl9012mnop3456
  |--@tag_Role_webserver:
  |  |--i-0abcd1234efgh5678
  |--@tag_Role_database:
  |  |--i-0ijkl9012mnop3456
  |--@instance_type_t3_medium:
  |  |--i-0abcd1234efgh5678
```

### Combining Dynamic + Static Inventory

You can point Ansible at a *directory* containing multiple inventory sources — it merges them:

```
inventory/
├── aws_ec2.yml         # Dynamic — auto-discovered EC2 instances
└── group_vars/
    └── tag_Role_webserver.yml   # Static variables applied to the dynamic group
```

```bash
ansible-playbook -i inventory/ site.yml
```

```yaml
# inventory/group_vars/tag_Role_webserver.yml
ansible_user: ec2-user
ansible_ssh_private_key_file: ~/.ssh/prod-key.pem
http_port: 8080
```

This pattern — dynamic host *discovery* combined with static *group variable* files — is the standard production setup for AWS-based Ansible automation.


---

## 18. Ansible + AWS (Provisioning Example)

### What

Beyond just *configuring* existing AWS resources, the `amazon.aws` and `community.aws` collections let Ansible *provision* AWS infrastructure directly (create EC2 instances, security groups, S3 buckets, etc.) — similar in spirit to Terraform, but imperative/task-based rather than a dedicated state-tracked DSL.

### Why — Ansible vs Terraform for AWS Provisioning

This is a common point of confusion, so it's worth being explicit given your existing Terraform-heavy workflow:

| | Terraform | Ansible |
|---|---|---|
| **Primary purpose** | Infrastructure provisioning, with a tracked **state file** representing desired vs actual infra | Configuration management + orchestration; can provision, but has no state file |
| **How it detects drift** | Compares its state file against real cloud resources (`terraform plan`) | Re-checks actual system state at *every run* — no separate state file needed |
| **Best at** | Creating/destroying/updating cloud resources (VPCs, EKS clusters, IAM, RDS) | Configuring what's *inside* those resources (packages, files, services, app deploys) |
| **Typical real-world pairing** | Provisions the EC2 instances / EKS node groups | Bootstraps/configures the OS and app layer on top of what Terraform created |

**Recommendation:** for net-new cloud infrastructure, prefer Terraform (which you already use extensively) — it has purpose-built state management that Ansible lacks. Use Ansible's AWS modules mainly for **one-off imperative actions** (e.g., "cycle instances in this ASG," "snapshot this RDS instance before a migration") or for teams that intentionally avoid a separate IaC state file.

### How — Example: Provisioning an EC2 Instance

```yaml
---
- name: Provision and configure an EC2 web server
  hosts: localhost                          # Runs on the control node — talking to the AWS API, not SSHing anywhere yet
  connection: local
  gather_facts: false
  vars:
    aws_region: us-east-1

  tasks:
    - name: Create a security group
      amazon.aws.ec2_security_group:
        name: webserver-sg
        description: Allow HTTP/HTTPS/SSH
        region: "{{ aws_region }}"
        rules:
          - proto: tcp
            ports: [22]
            cidr_ip: 10.0.0.0/16
          - proto: tcp
            ports: [80, 443]
            cidr_ip: 0.0.0.0/0
      register: sg_result

    - name: Launch EC2 instance
      amazon.aws.ec2_instance:
        name: web1
        key_name: my-keypair
        instance_type: t3.medium
        image_id: ami-0abcdef1234567890
        region: "{{ aws_region }}"
        security_group: "{{ sg_result.group_id }}"
        wait: true                            # Wait until the instance reaches "running" state
        tags:
          Environment: production
          Role: webserver
      register: ec2_result

    - name: Add the new instance to an in-memory inventory group for the NEXT play
      ansible.builtin.add_host:
        name: "{{ ec2_result.instances[0].public_ip_address }}"
        groups: just_provisioned
        ansible_user: ec2-user
        ansible_ssh_private_key_file: ~/.ssh/my-keypair.pem

    - name: Wait for SSH to become available
      ansible.builtin.wait_for:
        host: "{{ ec2_result.instances[0].public_ip_address }}"
        port: 22
        delay: 10
        timeout: 300

- name: Configure the newly-provisioned instance
  hosts: just_provisioned                     # This targets the group created dynamically above
  become: true
  roles:
    - nginx
```

This pattern — **Play 1 provisions infra + registers hosts in-memory via `add_host`; Play 2 immediately configures them** — is the idiomatic way to do provision-then-configure entirely within a single Ansible run, without needing a separate dynamic inventory refresh.

### Other Common AWS Modules

| Module | Purpose |
|---|---|
| `amazon.aws.s3_bucket` | Create/manage S3 buckets |
| `amazon.aws.ec2_instance` | Create/manage/terminate EC2 instances |
| `amazon.aws.ec2_security_group` | Manage security groups and rules |
| `amazon.aws.rds_instance` | Manage RDS database instances |
| `amazon.aws.iam_role` | Manage IAM roles/policies |
| `amazon.aws.autoscaling_group` | Manage Auto Scaling Groups |
| `community.aws.route53` | Manage Route53 DNS records |
| `kubernetes.core.k8s` | Apply Kubernetes manifests (useful for post-EKS-provisioning bootstrap, e.g. installing ArgoCD via Ansible as part of a larger pipeline) |


---

## 19. Directory Structure & Best Practices

### What

A recommended, community-standard layout for organizing a real-world Ansible project (this is the official layout recommended by Ansible's own documentation for multi-environment projects).

### Why

Consistent structure makes projects navigable for new contributors, keeps environment-specific config cleanly separated (dev/staging/prod), and avoids common footguns like accidentally applying dev variables to production.

### How

```
ansible-project/
├── ansible.cfg                    # Project-level configuration (overrides global defaults)
├── requirements.yml                # Pinned collection/role dependencies
├── site.yml                        # Master playbook — imports other playbooks
├── webservers.yml                  # Playbook targeting only webservers
├── dbservers.yml                   # Playbook targeting only dbservers
│
├── inventories/
│   ├── production/
│   │   ├── hosts.yml                # Static or dynamic (aws_ec2.yml) inventory
│   │   ├── group_vars/
│   │   │   ├── all.yml              # Vars for ALL hosts in this environment
│   │   │   ├── webservers.yml
│   │   │   └── dbservers.yml
│   │   └── host_vars/
│   │       └── web1.example.com.yml # Vars for one SPECIFIC host
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
│           └── all.yml
│
├── group_vars/                      # Vars applying across ALL inventories (rare — usually per-inventory is preferred)
│
├── roles/
│   ├── nginx/
│   ├── postgresql/
│   └── common/                       # Shared baseline config (users, security hardening, monitoring agents)
│
├── files/                            # Static files not tied to any specific role
├── templates/                        # Shared Jinja2 templates not tied to any specific role
│
└── library/                          # Custom, project-specific modules (rare — advanced use case)
```

### `ansible.cfg` — Project Configuration

```ini
# ansible.cfg
[defaults]
inventory = inventories/production/hosts.yml
roles_path = roles/
remote_user = ec2-user
host_key_checking = False        # Convenient for ephemeral cloud instances; disable carefully (security tradeoff)
forks = 20
retry_files_enabled = False
stdout_callback = yaml            # More readable output than the default
interpreter_python = auto_silent

[privilege_escalation]
become = True
become_method = sudo
become_ask_pass = False

[ssh_connection]
pipelining = True                 # Performance optimization — reduces SSH operations per task
control_path = ~/.ssh/ansible-%%h-%%p-%%r
```

> Ansible looks for `ansible.cfg` in this order: `ANSIBLE_CONFIG` env var → `./ansible.cfg` (current directory) → `~/.ansible.cfg` → `/etc/ansible/ansible.cfg`. The first one found wins — the rest are ignored entirely (they don't merge).

### Running Environment-Specific Playbooks

```bash
# Production
ansible-playbook -i inventories/production/hosts.yml site.yml

# Staging
ansible-playbook -i inventories/staging/hosts.yml site.yml
```

### Best Practices Checklist

- ✅ Pin collection/role versions in `requirements.yml` — never rely on "latest."
- ✅ Use `--check --diff` before every production run to preview changes.
- ✅ Keep secrets exclusively in Vault-encrypted files — never plaintext, ever, even temporarily.
- ✅ Name every task descriptively (`name:` field) — untitled tasks make output/logs unreadable.
- ✅ Prefer specific modules (`ansible.builtin.package`, `ansible.builtin.service`) over `shell`/`command` wherever a purpose-built module exists — you get idempotency and clearer diffs for free.
- ✅ Use `roles/common` for baseline configuration (users, SSH hardening, monitoring agents, timezone) applied to every single host.
- ✅ Run `ansible-lint` in CI to catch style/security issues automatically.
- ✅ Tag destructive/rarely-needed tasks with `never` so they require explicit opt-in.
- ✅ Use `serial` for production rollouts — never deploy to 100% of a fleet simultaneously.


---

## 20. CI/CD Integration

### What

Running Ansible playbooks automatically from a CI/CD pipeline (e.g., GitHub Actions) rather than manually from an engineer's laptop — ensuring consistent, auditable, repeatable deployments triggered by code changes.

### Why

Manual `ansible-playbook` runs from individual laptops suffer from "works on my machine," inconsistent collection versions, and no audit trail of who ran what, when. Pushing execution into CI/CD gives you: a single source of truth for the exact command that ran, credentials that never touch a developer's laptop, and a natural place to gate production changes behind approvals/tests — the same rationale you already apply to Terraform via CI/CD.

### How — GitHub Actions Example

```yaml
# .github/workflows/ansible-deploy.yml
name: Ansible Deploy

on:
  push:
    branches: [main]
    paths:
      - 'roles/**'
      - 'inventories/**'
      - '*.yml'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Ansible + ansible-lint
        run: pip install ansible ansible-lint
      - name: Lint playbooks
        run: ansible-lint site.yml

  deploy:
    needs: lint
    runs-on: ubuntu-latest
    environment: production          # Enables GitHub's manual approval gate for production
    steps:
      - uses: actions/checkout@v4

      - name: Install Ansible and dependencies
        run: |
          pip install ansible boto3 botocore
          ansible-galaxy collection install -r requirements.yml

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Set up SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key

      - name: Set up Vault password
        run: echo "${{ secrets.ANSIBLE_VAULT_PASSWORD }}" > .vault_pass.txt

      - name: Dry run first (fail fast before touching prod)
        run: |
          ansible-playbook -i inventories/production/aws_ec2.yml site.yml \
            --private-key ~/.ssh/deploy_key \
            --vault-password-file .vault_pass.txt \
            --check --diff

      - name: Apply for real
        run: |
          ansible-playbook -i inventories/production/aws_ec2.yml site.yml \
            --private-key ~/.ssh/deploy_key \
            --vault-password-file .vault_pass.txt

      - name: Clean up secrets
        if: always()                   # Runs even if previous steps failed — prevents leaking secrets in the runner's leftover filesystem
        run: rm -f .vault_pass.txt ~/.ssh/deploy_key
```

### Key CI/CD Patterns

| Pattern | Why |
|---|---|
| **Lint before deploy** | Catches YAML syntax errors, deprecated modules, and style issues before they reach production |
| **`--check --diff` as a separate step** | Produces a reviewable "plan" analogous to `terraform plan` — lets a human sanity-check before the real run |
| **GitHub Environment approval gates** | Requires manual sign-off before production deploys execute, same governance model as protected Terraform Cloud workspaces |
| **Secrets via GitHub Actions Secrets, never in the repo** | SSH keys, AWS credentials, and the Vault password are injected at runtime and never touch source control |
| **`if: always()` cleanup step** | Ensures decrypted secrets/keys are wiped from the runner's disk regardless of success/failure |


---

## 21. Troubleshooting Guide

| Symptom | Likely Cause | Fix |
|---|---|---|
| `UNREACHABLE! ... Permission denied (publickey)` | Wrong SSH key, or key not added to the target's `~/.ssh/authorized_keys` | Verify with `ssh -i key.pem user@host` manually first; check `ansible_ssh_private_key_file` in inventory |
| `UNREACHABLE! ... Failed to connect ... Connection timed out` | Security group / firewall blocking port 22, or wrong IP | Check security group inbound rules; verify `ansible_host` value |
| `"module_stderr": "/bin/sh: python3: command not found"` | Target host has no Python 3 (common on minimal/hardened AMIs) | Set `ansible_python_interpreter=/usr/bin/python3.9` (or correct path) as a host/group var |
| Task always reports `changed`, even when nothing actually changed | Using `command`/`shell` instead of an idempotent purpose-built module | Switch to `ansible.builtin.package`, `service`, `copy`, etc.; or add explicit `changed_when` logic |
| `fatal: ... "msg": "the field 'args' has an invalid value"` | YAML indentation error, usually mixing tabs/spaces or misaligned list items | Run `ansible-playbook --syntax-check`; check indentation consistency |
| Variable shows as `{{ my_var }}` literally in output, not substituted | Variable not defined in any active scope, or typo in variable name | Run with `-vvv` to see variable resolution; check `ansible_facts`/`vars` precedence order |
| Handler never fires | Notified task didn't actually report `changed`, or handler name doesn't exactly match `notify:` string | Confirm task shows `changed` in output; handler names are case-sensitive and must match exactly |
| `ansible-vault` fails with `Decryption failed` | Wrong vault password, or file corrupted/partially edited outside Vault | Re-verify password; check the file wasn't manually edited (breaks the AES256 header) |
| Playbook run hangs indefinitely | Task waiting on interactive prompt (e.g. `apt` asking for confirmation), or firewall silently dropping packets (vs. rejecting) | Add `-e DEBIAN_FRONTEND=noninteractive`, or press Ctrl+C and re-run with `-vvv` to see where it's stuck |
| `"msg": "MODULE FAILURE\nSee stdout/stderr..."` | Underlying module crashed, often due to unsupported OS or missing dependency on target | Run with `-vvv`, inspect `module_stdout`/`module_stderr` in output for the real Python traceback |
| Dynamic AWS inventory returns zero hosts | IAM permissions missing (`ec2:DescribeInstances`), or filters too restrictive, or wrong region | Test with `aws ec2 describe-instances --region <region>` using the same credentials; loosen `filters:` temporarily |
| Roles not found: `ERROR! the role 'nginx' was not found` | `roles_path` misconfigured, or role not installed via `ansible-galaxy` | Check `ansible.cfg` `roles_path`; run `ansible-galaxy install -r requirements.yml` |

### Essential Debugging Commands

```bash
# Maximum verbosity — shows full module input/output, SSH commands, connection details
ansible-playbook site.yml -vvvv

# Step through a playbook task-by-task, confirming each one interactively
ansible-playbook site.yml --step

# Print the value of any variable/fact for debugging
- name: Debug a variable
  ansible.builtin.debug:
    var: my_variable

- name: Debug with a custom message
  ansible.builtin.debug:
    msg: "The value is {{ my_variable }} and the host is {{ inventory_hostname }}"

# Validate playbook syntax without running it
ansible-playbook site.yml --syntax-check

# Show exactly what module calls WOULD be made, without connecting to any host
ansible-playbook site.yml --list-tasks
ansible-playbook site.yml --list-hosts
```


---

## 22. Command Cheat Sheet

### Installation & Setup

```bash
pip3 install --user ansible          # Install Ansible (control node only)
ansible --version                    # Verify install + show config file location
ansible-config dump --only-changed   # Show non-default config settings in effect
```

### Inventory

```bash
ansible-inventory -i inventory.ini --list      # Full JSON dump of inventory
ansible-inventory -i inventory.ini --graph     # Tree view of groups/hosts
ansible all -i inventory.ini --list-hosts      # Just the hostnames
```

### Ad-Hoc Commands

```bash
ansible all -i inventory.ini -m ping                                  # Connectivity check
ansible webservers -i inventory.ini -m setup                          # Gather facts
ansible all -i inventory.ini -m shell -a "uptime"                     # Run a shell command
ansible all -i inventory.ini -m package -a "name=git state=present" --become
ansible all -i inventory.ini -m service -a "name=nginx state=restarted" --become
ansible all -i inventory.ini -m copy -a "src=./f.txt dest=/tmp/f.txt"
```

### Playbooks

```bash
ansible-playbook site.yml -i inventory.ini                  # Run
ansible-playbook site.yml --check --diff                    # Dry-run + show diffs
ansible-playbook site.yml --syntax-check                    # Validate YAML/syntax only
ansible-playbook site.yml --list-tasks                      # Preview task list
ansible-playbook site.yml --list-hosts                      # Preview targeted hosts
ansible-playbook site.yml --limit web1.example.com          # Restrict to specific host(s)
ansible-playbook site.yml --tags deploy --skip-tags firewall
ansible-playbook site.yml -e "app_version=2.0"               # Pass extra vars
ansible-playbook site.yml --start-at-task="Install nginx"    # Resume from a specific task
ansible-playbook site.yml -vvv                                # Verbose debugging
ansible-playbook site.yml --step                              # Confirm each task interactively
```

### Vault

```bash
ansible-vault create secrets.yml
ansible-vault edit secrets.yml
ansible-vault view secrets.yml
ansible-vault encrypt vars/prod.yml
ansible-vault decrypt vars/prod.yml
ansible-vault rekey secrets.yml
ansible-vault encrypt_string 'value' --name 'var_name'
ansible-playbook site.yml --ask-vault-pass
ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt
```

### Galaxy

```bash
ansible-galaxy init roles/my-role                      # Scaffold a new role
ansible-galaxy collection install amazon.aws           # Install a collection
ansible-galaxy role install geerlingguy.nginx          # Install a role
ansible-galaxy install -r requirements.yml             # Install everything pinned in requirements.yml
ansible-galaxy collection list                         # List installed collections
```

### Linting

```bash
ansible-lint site.yml
yamllint site.yml
```

---

## Summary — Mental Model Recap

```
Inventory  →  WHO to target (hosts, groups)
Variables  →  WHAT values to use (per host/group/environment)
Modules    →  WHAT ACTION to take (install, copy, restart...) — idempotent building blocks
Tasks      →  ONE call to a module with specific arguments
Playbooks  →  ORDERED lists of tasks/plays — the automation script itself
Roles      →  REUSABLE, packaged bundles of tasks+templates+vars+handlers
Handlers   →  Tasks that fire ONLY when notified by a change
Vault      →  Encryption for secrets so they're safe to commit to Git
Dynamic Inventory → Live-queried hosts (e.g. from AWS) instead of a static file
```

If you remember nothing else: **Ansible describes desired state, checks current state, and only acts when the two differ.** Everything else — modules, idempotency, handlers, `--check` mode — exists in service of that one idea.