================================================================================
DETAILED STEP-BY-STEP: ADD JENKINS AGENT VIA SSH WITH PRIVATE KEY
================================================================================

Complete elaboration with explanations, examples, and troubleshooting for each step.

================================================================================
STEP 1: PREPARE THE REMOTE MACHINE (172.31.24.63)
================================================================================

WHY THIS STEP?
  Before Jenkins can connect to the remote machine, it needs:
  - A way to authenticate (SSH key)
  - Java runtime to execute jobs
  - A working directory for agent operations
  - Proper directory permissions

DETAILED BREAKDOWN:

1.1 ESTABLISH SSH CONNECTION TO REMOTE MACHINE
===============================================

What you're doing:
  Opening a terminal connection to the remote machine at 172.31.24.63

Command:
  ssh ubuntu@172.31.24.63

Explanation:
  - ubuntu = the username on the remote machine
  - 172.31.24.63 = the IP address of the remote machine
  - If using a different SSH key file:
    ssh -i /path/to/pem-key-1 ubuntu@172.31.24.63

Expected output (first time):
  The authenticity of host '172.31.24.63 (172.31.24.63)' can't be established.
  ED25519 key fingerprint is SHA256:abc123...
  Are you sure you want to continue connecting (yes/no/[fingerprint])?
  
  Type: yes
  
  Then if key-based auth works, you'll get a shell prompt:
  ubuntu@ip-172-31-24-63:~$

Troubleshooting:
  ❌ "Permission denied (publickey,password)" 
     = Your SSH key isn't set up yet. You may need to use password auth first.
  
  ❌ "Connection refused"
     = SSH server isn't running or wrong IP
  
  ❌ "Connection timed out"
     = Network connectivity issue or firewall blocking port 22

---

1.2 INSTALL JAVA ON REMOTE MACHINE
===================================

Why needed:
  Jenkins agent is a Java application. Without Java, the agent can't run.

Commands to run (on the remote machine):
  
  # Update package manager
  sudo apt update
  
  # Install Java Development Kit (JDK)
  # Using OpenJDK 17 (recommended for modern Jenkins)
  sudo apt install -y openjdk-17-jre-headless
  
  # Verify installation
  java -version

Expected output from "java -version":
  openjdk version "17.0.x" 2021-09-14
  OpenJDK Runtime Environment (build 17.0.x+x-post-Ubuntu-xxx)
  OpenJDK 64-Bit Server VM (build 17.0.x+x-post-Ubuntu-xxx, mixed mode, sharing)

Explanation of command flags:
  -y = automatically answer "yes" to any prompts
  openjdk-17-jre-headless = Java Runtime Environment without GUI (suitable for servers)

Alternative Java versions:
  # If you need Java 11:
  sudo apt install -y openjdk-11-jre-headless
  
  # If you need Java 8 (legacy):
  sudo apt install -y openjdk-8-jre-headless

Important:
  Match Java version on agent with Java version on Jenkins controller for best compatibility.
  Check Jenkins controller version:
    Go to Jenkins > Manage Jenkins > System Information
    Look for "Java Version"

Verify again:
  After installation, run:
    which java         # Shows Java path: /usr/bin/java
    java -version      # Shows version details

---

1.3 CREATE JENKINS USER (OPTIONAL BUT RECOMMENDED)
==================================================

Why:
  Running the agent as a dedicated "jenkins" user is a security best practice.
  Instead of using "ubuntu" user, you'll have a separate account for Jenkins.

Commands:
  # Create user 'jenkins' with home directory
  sudo useradd -m -s /bin/bash jenkins
  
  # Add jenkins to sudo group (optional, only if agent needs sudo)
  sudo usermod -aG sudo jenkins
  
  # Verify user was created
  cat /etc/passwd | grep jenkins

Expected output:
  jenkins:x:1001:1001::/home/jenkins:/bin/bash

Explanation:
  -m = create home directory at /home/jenkins
  -s /bin/bash = set shell to bash (not sh or nologin)
  -aG = add to additional group (sudo)

If you skip this step:
  Just use "ubuntu" user instead of "jenkins" user in all subsequent steps.

Check if jenkins user was created:
  id jenkins
  
  Output should show:
  uid=1001(jenkins) gid=1001(jenkins) groups=1001(jenkins)

---

1.4 CREATE .SSH DIRECTORY AND SETUP PUBLIC KEY
==============================================

What this does:
  Creates a .ssh directory where SSH keys are stored, then adds your public key
  to authorize SSH connections.

Commands (if using 'ubuntu' user):
  # Create .ssh directory
  mkdir -p ~/.ssh
  
  # Set strict permissions (required for SSH security)
  chmod 700 ~/.ssh
  
  # Create authorized_keys file
  touch ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys

Commands (if using 'jenkins' user):
  sudo mkdir -p /home/jenkins/.ssh
  sudo chmod 700 /home/jenkins/.ssh
  sudo chown jenkins:jenkins /home/jenkins/.ssh
  sudo touch /home/jenkins/.ssh/authorized_keys
  sudo chmod 600 /home/jenkins/.ssh/authorized_keys

Explanation of permissions:
  chmod 700 = only owner (ubuntu/jenkins) can read/write/execute
  chmod 600 = only owner can read/write (no execute for files)
  
  These strict permissions are REQUIRED by SSH for security.
  If permissions are wrong, SSH will refuse to work.

---

1.5 EXTRACT AND ADD YOUR PUBLIC KEY
===================================

What you're doing:
  Converting your private key to its corresponding public key,
  then adding it to authorized_keys file on the remote machine.

On your LOCAL MACHINE (where you have pem-key-1):
  
  # Extract public key from your RSA private key
  ssh-keygen -y -f pem-key-1
  
  Expected output:
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZndXzFDX....... user@hostname

This is your public key. Now copy the ENTIRE output.

On the REMOTE MACHINE (172.31.24.63):
  
  # If using ubuntu user, paste the public key:
  cat >> ~/.ssh/authorized_keys << 'EOF'
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZndXzFDX....... user@hostname
  EOF
  
  # If using jenkins user:
  sudo bash -c 'cat >> /home/jenkins/.ssh/authorized_keys << '"'"'EOF'"'"'
  ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZndXzFDX....... user@hostname
  EOF'

Verify it was added:
  # Check file contents
  cat ~/.ssh/authorized_keys
  
  # You should see your public key listed

Verify SSH key authentication works:
  # From your LOCAL MACHINE, test without password:
  ssh -i pem-key-1 ubuntu@172.31.24.63
  
  # Should connect WITHOUT asking for password
  # If successful, you see: ubuntu@ip-172-31-24-63:~$

---

1.6 CREATE JENKINS AGENT WORKING DIRECTORY
==========================================

What this is:
  A directory where Jenkins agent will store files, logs, and job workspaces.
  This is set as "Remote root directory" in Jenkins.

Commands (for ubuntu user):
  # Create directory
  mkdir -p ~/jenkins-agent
  
  # Set permissions
  chmod 700 ~/jenkins-agent
  
  # Verify
  ls -la ~/ | grep jenkins-agent

Commands (for jenkins user):
  sudo mkdir -p /home/jenkins/jenkins-agent
  sudo chown jenkins:jenkins /home/jenkins/jenkins-agent
  sudo chmod 700 /home/jenkins/jenkins-agent

Explanation:
  ~/jenkins-agent = /home/ubuntu/jenkins-agent or /home/jenkins/jenkins-agent
  chmod 700 = only the owner can access this directory
  
  This directory will contain:
  - Job workspaces
  - Build logs
  - Temporary files
  - Artifacts

Verify space available:
  df -h
  
  Should show at least 2-5 GB free space.

---

1.7 TEST SSH CONNECTION FROM JENKINS CONTROLLER
===============================================

What this does:
  Verifies that key-based authentication is working correctly
  before configuring Jenkins.

On the JENKINS CONTROLLER machine, run:
  
  # Using verbose mode to see connection details
  ssh -i /path/to/pem-key-1 -v ubuntu@172.31.24.63
  
  Replace /path/to/pem-key-1 with actual path to your private key.

What you should see:
  OpenSSH_8.0p1, LibSSL 1.1.1 ...
  debug1: Reading configuration data /home/user/.ssh/config
  debug1: No more authentication methods to try.
  Permission denied (publickey).
  
  OR (if successful):
  debug1: Authentication succeeded (publickey).
  Last login: Mon Feb 24 17:30:00 2026 from 192.168.1.100
  ubuntu@ip-172-31-24-63:~$

If successful:
  - Type: exit
  - You're now ready for Jenkins configuration

If it fails, troubleshoot:
  
  Problem: "Permission denied (publickey)"
  Solution:
    1. Verify public key is in authorized_keys:
       ssh ubuntu@172.31.24.63 "cat ~/.ssh/authorized_keys"
    2. Check permissions on remote machine:
       ssh ubuntu@172.31.24.63 "ls -la ~/.ssh"
       Should show: drwx------ (700) for .ssh, -rw------- (600) for authorized_keys
    3. Verify you're using correct private key:
       ssh-keygen -y -f pem-key-1
       Compare output with what's in authorized_keys
  
  Problem: "Connection refused"
  Solution:
    1. Check SSH service is running on remote:
       sudo systemctl status ssh
    2. Restart SSH if needed:
       sudo systemctl restart ssh
    3. Check SSH is listening on port 22:
       sudo netstat -tulpn | grep :22
  
  Problem: "Connection timeout"
  Solution:
    1. Verify connectivity:
       ping 172.31.24.63
    2. Check firewall:
       sudo ufw status
       sudo ufw allow 22/tcp  # If needed
    3. Check security groups (if AWS):
       Ensure inbound rule allows port 22 from Jenkins controller IP

================================================================================
STEP 2: ADD SSH CREDENTIALS IN JENKINS
================================================================================

WHY THIS STEP?
  Jenkins needs to store your SSH private key securely so it can authenticate
  to the remote machine. This step creates a credential object in Jenkins.

IMPORTANT NOTES:
  - Jenkins encrypts credentials in its database
  - Never paste credentials in plain text anywhere else
  - The credential ID (pem-key-1) is used to reference this key later

DETAILED BREAKDOWN:

2.1 NAVIGATE TO JENKINS CREDENTIALS PAGE
=========================================

Method 1: Via GUI
  1. Open Jenkins in web browser (http://your-jenkins:8080)
  2. Click "Manage Jenkins" in left sidebar
  3. Click "Manage Credentials"
  4. Should see credentials management page

Method 2: Direct URL
  Navigate to:
  http://your-jenkins:8080/credentials/

What you should see:
  A page showing credential stores. Default is:
  - System
    - Global credentials (unrestricted)

---

2.2 SELECT THE CREDENTIAL STORE
===============================

Navigate to where credentials are stored:
  1. Click on "System" link
  2. Click on "Global credentials (unrestricted)"

Why global?
  Global scope means this credential can be used by ANY Jenkins job on ANY node.
  This is convenient for agent setup.

Other scopes (for reference):
  - Global (Jenkins, nodes, items, all child items, etc) = Available everywhere
  - System (Jenkins and nodes only) = Can't be used by jobs
  - User credentials = Only available to specific user

---

2.3 CREATE NEW CREDENTIAL
=========================

Click "Add Credentials" button (top-left corner)

You'll see a form with these dropdown selections:
  - Kind
  - Scope
  - ID
  - Description
  - Username
  - Private Key
  - Passphrase

---

2.4 FILL IN CREDENTIAL FORM - STEP BY STEP
===========================================

Field 1: KIND
  Dropdown: Select "SSH Username with private key"
  
  Why this one?
  - "SSH Username with private key" = Using private key file (what we need)
  - Not "Username with password" (not using password auth)
  - Not "SSH key (Implicit)" (requires different setup)

Field 2: SCOPE
  Dropdown: Select "Global (Jenkins, nodes, items, all child items, etc)"
  
  Why global?
  - Makes credential available to all agents and jobs
  - Easiest to manage for agent configuration

Field 3: ID
  Text field: Enter "pem-key-1"
  
  What is this?
  - Unique identifier for this credential
  - Used in Jenkins pipelines and job configs
  - Cannot contain spaces
  - Example IDs: pem-key-1, aws-key, ec2-agent-key
  - You'll see this ID when selecting credentials in node config
  
  Important:
  - ID is NOT secret (visible in configs)
  - It's just a label/reference
  - The actual private key is stored securely

Field 4: DESCRIPTION
  Text field: Enter "EC2 Agent SSH Key for 172.31.24.63"
  
  Purpose:
  - Human-readable description of what this key is for
  - Helps identify correct credential when multiple exist
  - Example descriptions:
    "Production EC2 instance private key"
    "Dev agent at 10.0.1.50"
    "Staging server SSH key"

Field 5: USERNAME
  Text field: Enter "ubuntu"
  
  What is this?
  - The login username on the remote machine
  - This is the user that will run the Jenkins agent
  - Must exist on remote machine (we created it in Step 1)
  - Examples: ubuntu, ec2-user, jenkins, root
  
  Match with remote machine:
  - If remote machine uses "ec2-user": enter "ec2-user"
  - If remote machine uses "ubuntu": enter "ubuntu"
  - If remote machine uses "jenkins": enter "jenkins"

Field 6: PRIVATE KEY
  Radio button options:
  - ○ Enter directly
  - ○ From Jenkins master ~/.ssh/id_rsa
  
  Select: "Enter directly" (first option)
  
  Why?
  - We're providing the key content explicitly
  - More portable across different Jenkins setups
  
  What to do:
  1. Click on "Enter directly" radio button
  2. A text area appears below
  3. Paste your ENTIRE private key content

Field 7: PASTE YOUR PRIVATE KEY
  
  Where to get it:
  - Open pem-key-1 file with text editor
  - Ctrl+A to select all
  - Ctrl+C to copy
  
  What to paste:
  The entire file, exactly as is:
  
  -----BEGIN RSA PRIVATE KEY-----
  MIIEpAIBAAKCAQEA2Z3F8xQ7xJpR9v...
  [many more lines of base64]
  ...abc123xyz==
  -----END RSA PRIVATE KEY-----
  
  IMPORTANT:
  - Include BEGIN and END lines
  - Don't add extra spaces or lines
  - Copy exactly as is from the file
  - If key is encrypted, it will have "ENCRYPTED" in second line

Field 8: PASSPHRASE
  Text field: Leave EMPTY unless your key is encrypted
  
  Scenario 1: Key is NOT encrypted (most common)
    Second line of key does NOT say "ENCRYPTED"
    Passphrase field: [LEAVE EMPTY]
  
  Scenario 2: Key IS encrypted
    Second line of key DOES say "Proc-Type: 4,ENCRYPTED"
    Passphrase field: [ENTER THE PASSWORD]
    
    Example if encrypted key:
    -----BEGIN RSA PRIVATE KEY-----
    Proc-Type: 4,ENCRYPTED
    DEK-Info: DES-EDE3-CBC,ABC123...
    
    Then enter passphrase to decrypt it.

---

2.5 SAVE THE CREDENTIAL
=======================

Click "Create" button at bottom

Expected result:
  - You're redirected back to credentials list
  - You should see "pem-key-1" listed
  - Status shows it was created successfully

Verify creation:
  - Go back to Global credentials
  - You should see "pem-key-1" in the list
  - Click on it to see details (won't show the actual key for security)

---

2.6 COMMON MISTAKES IN THIS STEP
================================

Mistake 1: Wrong Kind selection
  ❌ Selected "Username with password" instead of "SSH Username with private key"
  ✓ Solution: Delete and recreate with correct kind

Mistake 2: Forgot to paste BEGIN and END lines
  ❌ Pasted only the middle base64 part
  ✓ Solution: Include -----BEGIN RSA PRIVATE KEY----- and -----END----- lines

Mistake 3: Copied key with extra spaces
  ❌ Key has trailing spaces or extra newlines
  ✓ Solution: Clean up the file, paste carefully

Mistake 4: Using wrong username
  ❌ Entered "root" but remote machine uses "ubuntu"
  ✓ Solution: Check what user exists on remote machine

Mistake 5: Wrong scope
  ❌ Selected "System" scope
  ✓ Solution: Use "Global" scope for agent setup

---

2.7 VERIFY CREDENTIAL CAN BE USED
=================================

Jenkins will validate the credential when you save it.
If you see no errors, the credential is valid.

However, full validation happens when Jenkins tries to use it in Step 4.

================================================================================
STEP 3: CREATE AND CONFIGURE JENKINS AGENT NODE
================================================================================

WHY THIS STEP?
  A "node" or "agent" in Jenkins is a machine that runs jobs.
  This step creates a configuration that tells Jenkins:
  - There's a new machine at 172.31.24.63
  - How to connect to it (SSH)
  - Where to store job files
  - How many jobs it can run in parallel

DETAILED BREAKDOWN:

3.1 NAVIGATE TO NODE MANAGEMENT
===============================

Method 1: Via GUI
  1. Click "Manage Jenkins" in left sidebar
  2. Click "Manage Nodes and Clouds"
  3. Should show a page with existing nodes (usually just "built-in node")

Method 2: Direct URL
  Navigate to:
  http://your-jenkins:8080/computer/

What you should see:
  - A list of existing nodes
  - "Built-in Node" is the Jenkins controller itself
  - A button to create new node

---

3.2 CREATE NEW NODE
===================

Click "New Node" button (or "Create a new node")

You'll see a form asking:

Question 1: Node name
  Text field: Enter "agent-172-31-24-63"
  
  What is this?
  - The identifier for this agent
  - Should be descriptive and unique
  - Examples:
    "agent-172-31-24-63"
    "ec2-prod-agent-1"
    "linux-build-agent"
  
  Rules:
  - No spaces
  - No special characters (except - and _)
  - Should reflect the agent's purpose or location

Question 2: Type of node
  Radio buttons:
  - ○ Permanent Agent
  - ○ Temporary Agent
  
  Select: "Permanent Agent"
  
  Why Permanent?
  - Stays configured even when Jenkins restarts
  - Permanent = always available
  - Temporary = ephemeral, disappears on restart

Question 3: Click Create
  After entering name and selecting type, click "Create"

---

3.3 CONFIGURE NODE PROPERTIES - EXECUTOR SETTINGS
==================================================

You'll now see the node configuration form with many fields.

Field 1: Number of executors
  Default: 2
  Current value: 1
  
  What is this?
  - How many jobs can run in parallel on this agent
  - Each executor can run one job at a time
  - Value 2 = 2 jobs can run simultaneously
  
  How to set:
  - If agent has 4 CPU cores: set to 4
  - If agent has 2 CPU cores: set to 2
  - If unsure: start with 2
  
  Check on remote machine:
  nproc  # Returns number of CPU cores
  
  Examples:
  - 1 executor = sequential job execution
  - 2 executors = 2 jobs in parallel
  - 4 executors = 4 jobs in parallel
  
  Memory consideration:
  - Each executor uses ~500MB-1GB of memory
  - 4 executors need ~2-4 GB of memory on agent
  - Adjust based on available resources

---

3.4 CONFIGURE NODE PROPERTIES - DIRECTORY SETTINGS
==================================================

Field 2: Remote root directory
  Current value: (empty)
  What to enter: /home/ubuntu/jenkins-agent
  
  What is this?
  - The working directory on the remote machine
  - All job workspaces will be stored here
  - This is the directory we created in Step 1.6
  
  Examples:
  - /home/ubuntu/jenkins-agent (for ubuntu user)
  - /home/jenkins/jenkins-agent (for jenkins user)
  - /var/lib/jenkins (alternative location)
  - /opt/jenkins (another alternative)
  
  Path rules:
  - Must be absolute path (starts with /)
  - Must exist on remote machine (we created it)
  - User running agent must have read/write permission
  - Should have at least 2-5 GB free space
  
  Verify on remote machine:
  ls -la /home/ubuntu/jenkins-agent
  
  Should show:
  drwx------ ... jenkins-agent

---

3.5 CONFIGURE NODE PROPERTIES - LABELS
=======================================

Field 3: Labels
  Current value: (empty)
  What to enter: agent docker linux
  
  What are labels?
  - Tags used to target jobs to specific agents
  - Multiple labels separated by spaces
  - Used in job configuration to specify "run on which agent?"
  
  Example labels to use:
  - agent = general purpose agent
  - docker = agent has Docker installed
  - linux = Linux operating system
  - prod = production environment
  - amd64 = processor type
  - 16gb = memory available
  
  How jobs use labels:
  In job configuration, "Restrict where this project can be run":
  Label Expression: "docker && linux"
  (This job runs on agents with BOTH docker AND linux labels)
  
  For testing, just use:
  Label Expression: "agent"

---

3.6 CONFIGURE NODE PROPERTIES - USAGE
=====================================

Field 4: Usage
  Dropdown options:
  - ○ Use this node as much as possible
  - ○ Only build jobs with label expressions matching this node
  
  Select: "Use this node as much as possible"
  
  Explanation:
  Option 1: "Use this node as much as possible"
    - Jenkins uses this agent for any job that doesn't specify labels
    - New jobs will run on this agent
    - Good for general purpose agent
  
  Option 2: "Only build jobs with label expressions matching this node"
    - Jenkins only uses this agent for jobs with matching labels
    - Other jobs run on built-in node
    - Good if you want strict job-to-agent assignment

For your first agent, use Option 1.

---

3.7 CONFIGURE LAUNCH METHOD - SSH LAUNCHER
===========================================

Field 5: Launch method
  Dropdown options:
  - ○ Launch agents via SSH
  - ○ Launch agents via Java Web Start
  - ○ Launch via SSH build wrapper plugin
  - ○ Launch slave agents via execution of command on the Master
  
  Select: "Launch agents via SSH"
  
  Why SSH?
  - Most secure and reliable method
  - Uses SSH protocol (port 22)
  - Our setup uses SSH key authentication
  - Best for production

---

3.8 CONFIGURE SSH SETTINGS - HOST
=================================

Field 6: Host
  Current value: (empty)
  What to enter: 172.31.24.63
  
  What is this?
  - The IP address or hostname of the remote machine
  - This is the machine Jenkins will SSH into
  - Port defaults to 22 (SSH standard port)
  
  Examples:
  - 172.31.24.63 (IP address)
  - ec2-instance.example.com (hostname)
  - agent.internal (internal DNS name)
  
  Verification:
  Before entering here, test connectivity:
  ping 172.31.24.63
  ssh ubuntu@172.31.24.63

---

3.9 CONFIGURE SSH SETTINGS - CREDENTIALS
========================================

Field 7: Credentials
  Dropdown: Select "pem-key-1"
  
  What is this?
  - The SSH credential we created in Step 2
  - Jenkins will use this key to authenticate
  - Dropdown shows all available SSH credentials
  
  What you'll see in dropdown:
  - pem-key-1 (ubuntu)
  - Any other SSH credentials you've created
  - (none) - if you haven't created credentials
  
  If pem-key-1 doesn't appear:
  - Go back to Step 2 and create the credential
  - Or click "Add" next to dropdown to create new one

---

3.10 CONFIGURE SSH SETTINGS - HOST KEY VERIFICATION
==================================================

Field 8: Host Key Verification Strategy
  Dropdown options:
  - ○ Non verifying Verification Strategy
  - ○ Known hosts file Verification Strategy
  - ○ Jenkins hosted Verification Strategy
  
  For testing (recommended for now):
  Select: "Non verifying Verification Strategy"
  
  Explanation:
  Non verifying strategy:
    - Jenkins doesn't check if host key is trusted
    - Faster connection
    - Less secure (vulnerable to man-in-the-middle)
    - OK for private networks, NOT for public internet
    - Gives warning in logs: "WARNING: SSH Host Keys are not being verified"
  
  Known hosts strategy (production):
    - Jenkins checks host key matches ~/.ssh/known_hosts
    - More secure
    - Requires setup of known_hosts file
    - More reliable for production
  
  We'll use Non-verifying for now to get it working.

---

3.11 CONFIGURE SSH SETTINGS - TIMEOUT AND RETRIES
================================================

Field 9: SSH Key Connection Timeout
  Default: 60 (seconds)
  What to enter: 60
  
  What is this?
  - How long Jenkins waits for SSH connection to establish
  - If connection takes longer, it times out
  - In seconds
  
  Values:
  - 30 seconds = short timeout (local network)
  - 60 seconds = standard (good default)
  - 120 seconds = long timeout (slow networks)
  
  If agent is over internet:
  - Increase to 120 seconds

Field 10: Max number of retries
  Default: 10
  What to enter: 10
  
  What is this?
  - If connection fails, how many times does Jenkins retry?
  - If first attempt fails, wait and try again
  - Helps handle temporary network issues
  
  Values:
  - 3 = minimal retries
  - 10 = default (recommended)
  - 20 = lots of retries (for flaky networks)

Field 11: Retry wait time
  Default: 15 (seconds)
  What to enter: 15
  
  What is this?
  - How long to wait between retry attempts
  - After first attempt fails, wait 15 seconds before retry
  - In seconds
  
  Values:
  - 5 seconds = quick retry
  - 15 seconds = standard (good balance)
  - 30 seconds = long wait between retries

---

3.12 CONFIGURE AVAILABILITY (OPTIONAL)
=======================================

Field 12: Availability
  Dropdown options:
  - ○ Keep this agent online as much as possible
  - ○ Bring this agent online according to a schedule
  - ○ Bring this agent online when in demand, and off otherwise
  
  Select: "Keep this agent online as much as possible"
  
  Explanation:
  Option 1: "Keep this agent online as much as possible"
    - Agent always tries to stay connected
    - Recommended for permanent agents
    - Agent reconnects if connection drops
  
  Option 2: "According to a schedule"
    - Agent only available during certain times
    - For agents you don't always need
  
  Option 3: "Online when in demand"
    - Agent starts when jobs need it
    - Saves resources but slower startup
    - Good for cloud agents
  
  For your first agent, use Option 1.

---

3.13 CONFIGURE TOOL LOCATIONS (OPTIONAL)
========================================

These are optional and can usually be left empty.

Field 13: JVM options
  Default: (empty)
  Examples:
  - -Xmx1024m (set max memory to 1GB)
  - -Xmx2048m (set max memory to 2GB)
  - -Duser.timezone=UTC (set timezone)
  
  Leave empty to use defaults.

Field 14: Java Path
  Default: (empty)
  Examples:
  - /usr/bin/java
  - /usr/lib/jvm/java-17-openjdk-amd64/bin/java
  
  Leave empty to auto-detect (recommended).

Field 15: Prefix Start Agent Command
  Default: (empty)
  Use case: Run commands BEFORE agent starts
  Example: export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  
  Leave empty unless needed.

Field 16: Suffix Start Agent Command
  Default: (empty)
  Use case: Run commands AFTER agent starts
  Example: source ~/.bashrc
  
  Leave empty unless needed.

---

3.14 SAVE CONFIGURATION
=======================

Scroll to bottom of page and click "Save" button

Expected result:
  - You're redirected to the node details page
  - You should see the node listed in "Manage Nodes and Clouds"
  - Status may show as OFFLINE initially (this is normal)

---

3.15 CONFIGURATION VERIFICATION
===============================

After saving, verify the configuration was saved:
  1. Go to "Manage Nodes and Clouds"
  2. Click on your agent "agent-172-31-24-63"
  3. Check that all your settings are there:
     ✓ Host: 172.31.24.63
     ✓ Remote root directory: /home/ubuntu/jenkins-agent
     ✓ Credentials: pem-key-1
     ✓ Executors: 2
     ✓ Labels: agent docker linux

================================================================================
STEP 4: START THE AGENT AND ESTABLISH CONNECTION
================================================================================

WHY THIS STEP?
  Now that the node is configured, Jenkins will attempt to SSH into the
  remote machine and launch the agent process.

DETAILED BREAKDOWN:

4.1 TRIGGER AGENT LAUNCH
========================

Option 1: Automatic launch
  Jenkins automatically attempts to launch the agent when:
  - The node is created
  - Jenkins restarts
  - Time interval passes
  
  Just wait 1-2 minutes and check status.

Option 2: Manual launch
  1. Go to "Manage Nodes and Clouds"
  2. Click on your node "agent-172-31-24-63"
  3. Click "Relaunch agent" button
  4. Jenkins starts the connection process

---

4.2 MONITOR THE CONNECTION LOG
==============================

What to look for:
  1. Click on your agent node
  2. Scroll down to see the log output
  3. Watch the connection process in real-time

Successful connection log example:
  [02/24/26 18:30:00] [SSH] Opening SSH connection to 172.31.24.63:22.
  [02/24/26 18:30:01] [SSH] SSH connection established.
  [02/24/26 18:30:01] [SSH] Initial agent handshake complete.
  [02/24/26 18:30:02] Agent successfully connected and online.

What each line means:
  "Opening SSH connection" = Jenkins is attempting to connect
  "SSH connection established" = Port 22 is reachable
  "Initial agent handshake" = SSH authentication successful
  "Agent successfully connected" = Agent Java process started
  "online" = Agent is ready to run jobs

---

4.3 COMMON CONNECTION ISSUES AND SOLUTIONS
=========================================

Issue 1: "Authentication failed"
  Log message:
    ERROR: Failed to authenticate as ubuntu (credentialId:pem-key-1/method:publickey)
    java.io.IOException: Publickey authentication failed.
  
  Causes:
    ❌ Public key not in authorized_keys on remote
    ❌ Wrong username in credential
    ❌ Key format wrong (OpenSSH vs RSA)
    ❌ Wrong private key in credential
  
  Solutions:
    1. Verify public key is on remote:
       ssh ubuntu@172.31.24.63 "cat ~/.ssh/authorized_keys"
    2. Extract and re-add public key:
       ssh-keygen -y -f pem-key-1
       Paste output to ~/.ssh/authorized_keys on remote
    3. Verify credential username matches remote user:
       Jenkins credential username = "ubuntu"
       Remote user = "ubuntu" (check with: whoami)
    4. Test SSH connection manually:
       ssh -i pem-key-1 -v ubuntu@172.31.24.63

Issue 2: "Connection timeout"
  Log message:
    [SSH] Opening SSH connection to 172.31.24.63:22.
    [SSH] Connection timed out.
  
  Causes:
    ❌ Remote machine is down
    ❌ Network unreachable
    ❌ Firewall blocking port 22
    ❌ SSH service not running on remote
  
  Solutions:
    1. Verify remote machine is running:
       ping 172.31.24.63
    2. Check SSH service:
       ssh ubuntu@172.31.24.63 "sudo systemctl status ssh"
    3. Check firewall:
       ssh ubuntu@172.31.24.63 "sudo ufw status"
       ssh ubuntu@172.31.24.63 "sudo ufw allow 22/tcp"
    4. Test port connectivity:
       telnet 172.31.24.63 22
       nc -zv 172.31.24.63 22
    5. Increase SSH timeout in Jenkins:
       Node config > SSH Key Connection Timeout = 120

Issue 3: "Java not found"
  Log message:
    [SSH] Checking Java version of /usr/bin/java
    [SSH] Java not found.
    [SSH] Checking Java version of ...
    ERROR: Could not find Java on the remote machine.
  
  Causes:
    ❌ Java not installed on remote
    ❌ Java installed but not in PATH
  
  Solutions:
    1. Install Java on remote:
       ssh ubuntu@172.31.24.63 "sudo apt install -y openjdk-17-jre-headless"
    2. Verify Java is installed:
       ssh ubuntu@172.31.24.63 "java -version"
    3. Find Java path:
       ssh ubuntu@172.31.24.63 "which java"
    4. If Java found, specify path in Jenkins:
       Node config > Java Path = /usr/bin/java

Issue 4: "PEM problem: it is of unknown type"
  Log message (from previous error you showed):
    Caused by: java.io.IOException: PEM problem: it is of unknown type.
    Supported algorithms are: [ssh-ed25519, ecdsa-sha2-nistp521, ...]
  
  Causes:
    ❌ Key is in OpenSSH format, not RSA/EC/Ed25519
    ❌ Key file corrupted
  
  Solutions:
    1. Check key format:
       head -1 pem-key-1
       Should show: -----BEGIN RSA PRIVATE KEY-----
    2. Convert if needed:
       ssh-keygen -p -m pem -f pem-key-1
    3. Re-upload key to Jenkins credential
    4. Test locally:
       openssl rsa -in pem-key-1 -check -noout

Issue 5: "Permission denied" - Directory access
  Log message:
    [SSH] Starting JNLP agent connection
    ERROR: java.io.IOException: Cannot create /home/ubuntu/jenkins-agent
  
  Causes:
    ❌ Remote root directory doesn't exist
    ❌ User doesn't have write permission
  
  Solutions:
    1. Create directory on remote:
       ssh ubuntu@172.31.24.63 "mkdir -p ~/jenkins-agent"
    2. Set permissions:
       ssh ubuntu@172.31.24.63 "chmod 700 ~/jenkins-agent"
    3. Verify:
       ssh ubuntu@172.31.24.63 "ls -la ~/ | grep jenkins-agent"

---

4.4 SUCCESSFUL CONNECTION INDICATORS
==================================

After successful connection, you should see:
  ✓ Node status shows green circle (online)
  ✓ Log shows "Agent successfully connected and online"
  ✓ Agent appears in "Manage Nodes and Clouds"
  ✓ Executors are available (shows "2 idle")

---

4.5 TROUBLESHOOTING WITH VERBOSE LOGGING
========================================

If connection fails and you need more details:

Method 1: Check Jenkins logs
  Jenkins main log:
  ~/.jenkins/logs/all.log
  (Or wherever Jenkins stores logs)

Method 2: Check agent logs
  On remote machine:
  tail -f /home/ubuntu/jenkins-agent/agent.log
  (If agent process started)

Method 3: Enable Jenkins debug logging
  Jenkins > Manage Jenkins > System Log > Add log recorder
  Logger: hudson.plugins.sshslaves
  Level: FINEST
  
  Then try to launch agent again, check debug output.

Method 4: Test SSH manually with verbose flag
  Jenkins controller:
  ssh -i /path/to/pem-key-1 -vvv ubuntu@172.31.24.63

================================================================================
STEP 5: TEST THE AGENT WITH A TEST JOB
================================================================================

WHY THIS STEP?
  Verify that the agent is working correctly and can actually execute jobs.

DETAILED BREAKDOWN:

5.1 CREATE A NEW TEST JOB
========================

1. Go to Jenkins Dashboard
2. Click "New Item" (or "Create Job")
3. Enter Job name: "Test-Agent"
4. Select job type: "Freestyle job"
5. Click "OK"

You'll see the job configuration page.

---

5.2 CONFIGURE JOB TO USE THE AGENT
==================================

In the job configuration page:

Find section: "General"
  ☑ Check box: "Restrict where this project can be run"
  
  After checking, new field appears:
  Label Expression: [agent]
  
  Enter: agent
  (This is the label we assigned to the agent node)
  
  Explanation:
  - Label Expression = "agent" means this job only runs on nodes with label "agent"
  - Our agent has label "agent docker linux"
  - Since it has "agent" label, it matches

---

5.3 ADD BUILD STEPS
===================

Find section: "Build"
  Click "Add build step"
  Select "Execute shell"
  
  In the command box, enter:
  
  #!/bin/bash
  set -e
  
  echo "=== Testing Jenkins Agent ==="
  echo "Hostname:"
  hostname
  
  echo -e "\nCurrent directory:"
  pwd
  
  echo -e "\nJava version:"
  java -version
  
  echo -e "\nUser running agent:"
  whoami
  
  echo -e "\nDisk space:"
  df -h | head -5
  
  echo -e "\nMemory:"
  free -h
  
  echo -e "\nAgent test completed successfully!"

---

5.4 SAVE THE JOB
================

Click "Save" button (bottom-right)

---

5.5 RUN THE TEST JOB
====================

1. You're back on job page
2. Click "Build Now" button (left sidebar)
3. Under "Build History", you should see a new build started
4. Click on the build number to see console output

---

5.6 MONITOR BUILD EXECUTION
===========================

In the console output, you'll see:

1. Job queued/started:
   "Started by user Admin"
   "Running as SYSTEM: Building in workspace /home/ubuntu/jenkins-agent/workspace/Test-Agent"

2. Build steps execute:
   "=== Testing Jenkins Agent ==="
   "Hostname: ip-172-31-24-63"
   "Current directory: /home/ubuntu/jenkins-agent/workspace/Test-Agent"
   "java version "17.0.5" 2022-10-18 LTS"
   "User running agent: ubuntu"
   [etc.]

3. Job completion:
   "Build succeeded" = Green checkmark ✓
   "Build failed" = Red X and error message

---

5.7 VERIFY EXECUTION WAS ON AGENT
=================================

What to look for in console output:

Line 1 should show workspace path:
  "Running in workspace /home/ubuntu/jenkins-agent/workspace/Test-Agent"
  
This indicates:
  ✓ Job ran on the agent machine
  ✓ Using correct remote root directory
  ✓ Files are in remote directory, not controller

Hostname should show remote machine:
  "Hostname: ip-172-31-24-63" (or whatever your remote hostname is)

User should be "ubuntu":
  "User running agent: ubuntu"

If job ran on controller instead:
  ✗ Workspace shows Jenkins controller path
  ✗ Hostname shows controller hostname
  Then labels aren't matching. Check agent labels.

---

5.8 CLEANUP TEST JOB
====================

After verifying success, you can delete the test job:
  1. Go to job
  2. Click "Delete Job" (left sidebar)
  3. Confirm deletion

---

5.9 TROUBLESHOOTING TEST JOB ISSUES
==================================

Issue: Build doesn't run on agent
  Log shows:
  "Running in workspace /var/lib/jenkins/workspace/Test-Agent"
  (This is controller, not agent!)
  
  Causes:
    ❌ Label expression doesn't match
    ❌ Agent is offline
    ❌ Agent has 0 executors
  
  Solutions:
    1. Verify agent is online:
       Manage Nodes and Clouds > Check status circle
    2. Verify agent has executors:
       Node config > Number of executors = 2
    3. Verify labels match:
       Job config > Label Expression = "agent"
       Node config > Labels = "agent docker linux"
    4. Restart the build:
       Click "Build Now" again

Issue: Build fails on agent
  Error in console output, but not on controller
  
  Causes:
    ❌ Different OS (Windows vs Linux commands)
    ❌ Missing tools on agent
    ❌ Different PATH or environment
  
  Solutions:
    1. Add echo statements to debug:
       echo "PATH: $PATH"
       echo "Environment:"
       env | sort
    2. Install missing tools:
       ssh ubuntu@172.31.24.63 "sudo apt install -y [tool]"
    3. Source shell configuration:
       source ~/.bashrc
       source ~/.profile

Issue: Build times out
  Log shows:
  "Build timed out"
  "Process terminated"
  
  Causes:
    ❌ Command takes too long
    ❌ Agent is slow
    ❌ Network issue between controller and agent
  
  Solutions:
    1. Increase job timeout:
       Job config > Build Timeout > Set time
    2. Simplify test commands
    3. Check agent machine resources:
       ssh ubuntu@172.31.24.63 "top -b -n 1"

================================================================================
STEP 6: COMPREHENSIVE TROUBLESHOOTING
================================================================================

This section covers advanced troubleshooting for various issues.

ISSUE: "Failed to authenticate as ubuntu"
=========================================

Detailed diagnostics:

Step 1: Verify SSH works from Jenkins controller
  
  SSH into Jenkins controller (or access shell)
  
  Test SSH connection:
  ssh -i /path/to/pem-key-1 -v ubuntu@172.31.24.63
  
  Look for output:
  - "debug1: Authentication succeeded (publickey)."
  
  If fails, the problem is with SSH setup, not Jenkins.

Step 2: Verify public key is on remote
  
  ssh ubuntu@172.31.24.63 "cat ~/.ssh/authorized_keys"
  
  You should see output starting with "ssh-rsa AAAA..."
  
  If empty or missing:
    ssh-keygen -y -f pem-key-1 > /tmp/pub.txt
    scp /tmp/pub.txt ubuntu@172.31.24.63:/tmp/
    ssh ubuntu@172.31.24.63 "cat /tmp/pub.txt >> ~/.ssh/authorized_keys"

Step 3: Verify permissions on remote
  
  ssh ubuntu@172.31.24.63 "ls -la ~/ | grep '.ssh'; ls -la ~/.ssh"
  
  Should show:
  drwx------ 2 ubuntu ubuntu 4096 Feb 24 18:00 .ssh
  -rw------- 1 ubuntu ubuntu 400  Feb 24 18:05 authorized_keys
  
  If permissions wrong:
    ssh ubuntu@172.31.24.63 "chmod 700 ~/.ssh; chmod 600 ~/.ssh/authorized_keys"

Step 4: Verify Jenkins credential is correct
  
  In Jenkins:
  1. Go to Manage Credentials
  2. Click on "pem-key-1"
  3. Click "Update"
  4. Check:
     - Username: ubuntu (matches remote user)
     - Private Key field has full key (BEGIN and END lines)
     - Passphrase is empty (unless key is encrypted)

Step 5: Try using username from credential
  
  In Jenkins node config:
  Look at SSH Credentials dropdown - it shows "pem-key-1 (ubuntu)"
  This confirms username is "ubuntu"

---

ISSUE: Agent connects, but builds run on wrong machine
====================================================

Your build runs on Jenkins controller instead of agent.

Step 1: Verify agent is online
  
  Manage Nodes and Clouds
  Look at status circle next to agent name:
    ✓ Green = online, ready to run jobs
    ❌ Red/orange = offline or limited capacity

Step 2: Verify job label configuration
  
  In job configuration:
  - Check "Restrict where this project can be run"
  - Label Expression: must match agent labels
  
  Agent labels: "agent docker linux"
  Job label: could be "agent", "docker", "linux", or "agent && docker"
  
  For debugging: use label "agent"

Step 3: Verify agent has available executors
  
  Manage Nodes and Clouds > Click agent name
  Should show: "2 executors" (or however many you configured)
  Should show: "2 idle" (if not running jobs)
  
  If shows "0", update node config to increase executors.

Step 4: Check Jenkins logs for label matching
  
  Jenkins logs often show:
  "No nodes matched the label expression"
  
  This means labels don't match. Verify:
  - Job label expression
  - Agent labels
  - Case sensitivity (labels are case-sensitive!)

Step 5: Test with explicit label
  
  For debugging:
  1. Go to agent > Configure
  2. Labels: agent-test
  3. Save
  4. Create new job
  5. Restrict where this project can be run
  6. Label Expression: agent-test
  7. Build Now
  
  If it works with "agent-test", but not "agent", then
  the original label might be typed wrong (spaces, case, etc.)

---

ISSUE: Agent disconnects randomly
=================================

Agent connects successfully but randomly disconnects and reconnects.

Step 1: Check agent machine resources
  
  ssh ubuntu@172.31.24.63 "top -b -n 1"
  
  Look for:
  - High CPU usage (>80%)
  - Low free memory (<100MB)
  - High disk usage (>90%)
  
  If resources exhausted, builds fill up disk/memory and crash agent.

Solution:
  - Increase machine resources (CPU, RAM, disk)
  - Reduce number of executors
  - Clean up old workspace directories

Step 2: Check network connectivity
  
  From Jenkins controller, monitor connection:
  ping -c 1000 172.31.24.63 | grep "% packet loss"
  
  If showing packet loss, network is unstable.
  
  Check:
    - Network interface errors: ethtool -S eth0
    - Cable/connection quality
    - Firewall rules resetting connections

Step 3: Check SSH timeout settings
  
  In Jenkins node config:
  - SSH Key Connection Timeout: increase to 120
  - Max number of retries: 20
  - Retry wait time: 30
  
  These settings help agent reconnect if temporary network issue.

Step 4: Check Jenkins system configuration
  
  Jenkins > Manage Jenkins > Configure System > SSH Launcher settings:
  
  Add system property to keep connection alive:
  -DclientKeepAliveInterval=30
  
  This sends keep-alive packets every 30 seconds.

Step 5: Monitor agent logs
  
  Check agent logs for errors:
  ssh ubuntu@172.31.24.63 "tail -f /home/ubuntu/jenkins-agent/*.log"
  
  Look for exceptions or errors that cause disconnection.

---

ISSUE: "Cannot find Java on remote machine"
==========================================

Step 1: Verify Java is installed
  
  ssh ubuntu@172.31.24.63 "java -version"
  
  Should output Java version information.
  
  If command not found:
    sudo apt update
    sudo apt install -y openjdk-17-jre-headless

Step 2: Find Java path
  
  ssh ubuntu@172.31.24.63 "which java"
  
  Output should be: /usr/bin/java
  
  Note down this path.

Step 3: Update Jenkins node config
  
  In Jenkins node configuration:
  Java Path: /usr/bin/java
  (Put the path from step 2)
  
  Save and try launching agent again.

Step 4: If Java still not found, specify JVM options
  
  Node config > JVM options:
  -Xmx1024m
  
  This sets Java max memory to 1GB, might help if Java is running but low memory.

---

ISSUE: "No such file or directory" for remote root directory
===========================================================

Step 1: Verify directory exists on remote
  
  ssh ubuntu@172.31.24.63 "ls -la /home/ubuntu/jenkins-agent"
  
  Should show directory listing.
  
  If "No such file or directory":
    mkdir -p /home/ubuntu/jenkins-agent
    chmod 700 /home/ubuntu/jenkins-agent

Step 2: Verify permissions
  
  ssh ubuntu@172.31.24.63 "ls -la ~/ | grep jenkins-agent"
  
  Should show:
  drwx------ ... jenkins-agent
  
  If different permissions:
    chmod 700 /home/ubuntu/jenkins-agent

Step 3: Verify free space
  
  ssh ubuntu@172.31.24.63 "df -h /home/ubuntu/"
  
  Should show at least 2-5 GB available.
  
  If full:
    - Delete old workspaces
    - Increase disk size
    - Use different directory

================================================================================
STEP 7: FINAL VERIFICATION AND CHECKLIST
================================================================================

Complete verification checklist to confirm everything is working.

CHECKLIST ITEMS:

Remote Machine Setup:
  ☑ SSH service is running
    Test: ssh ubuntu@172.31.24.63 "sudo systemctl status ssh"
  
  ☑ Java is installed
    Test: ssh ubuntu@172.31.24.63 "java -version"
  
  ☑ Jenkins agent directory exists
    Test: ssh ubuntu@172.31.24.63 "ls -la ~/jenkins-agent"
  
  ☑ Public key in authorized_keys
    Test: ssh ubuntu@172.31.24.63 "grep 'ssh-rsa' ~/.ssh/authorized_keys"
  
  ☑ Directory has correct permissions
    Test: ssh ubuntu@172.31.24.63 "ls -la ~/.ssh"
    Expected: drwx------ and -rw-------
  
  ☑ Sufficient disk space available
    Test: ssh ubuntu@172.31.24.63 "df -h /home/ubuntu/ | tail -1"
    Expected: >5GB free

Jenkins Credential Setup:
  ☑ SSH credential "pem-key-1" exists
    Test: Jenkins > Manage Credentials > Global > Look for pem-key-1
  
  ☑ Credential has correct username (ubuntu)
    Test: Click on credential, check username field
  
  ☑ Private key is complete (BEGIN and END lines)
    Test: Click credential > Update, check key starts with BEGIN

Jenkins Node Configuration:
  ☑ Node "agent-172-31-24-63" exists
    Test: Manage Nodes and Clouds > Look for node in list
  
  ☑ Node configuration matches:
    Test: Click node > Verify:
      - Host: 172.31.24.63
      - Credentials: pem-key-1
      - Remote root directory: /home/ubuntu/jenkins-agent
      - Executors: 2
      - Labels: agent docker linux
  
  ☑ Launch method is "SSH Launcher"
    Test: Node config > Launch method section shows SSH Launcher
  
  ☑ Node status is "Online"
    Test: Manage Nodes and Clouds > Green circle next to node name

Connection Testing:
  ☑ Agent connects successfully
    Test: Node page > Check log shows "Agent successfully connected and online"
  
  ☑ Agent shows executors available
    Test: Node page > Shows "2 idle" (or however many configured)
  
  ☑ SSH connection works manually
    Test: ssh -i pem-key-1 -v ubuntu@172.31.24.63
    Should connect without password

Job Execution:
  ☑ Test job runs on agent (not controller)
    Test: Build > Console output shows:
      "Running in workspace /home/ubuntu/jenkins-agent/workspace/Test-Agent"
  
  ☑ Test job shows correct hostname
    Test: Build > Console output shows:
      "hostname: ip-172-31-24-63" (remote hostname, not controller)
  
  ☑ Test job shows correct user
    Test: Build > Console output shows:
      "whoami: ubuntu"
  
  ☑ Build succeeded (green checkmark)
    Test: Build history shows green checkmark ✓

FINAL VERIFICATION COMMAND (on Jenkins controller):

Run this command to verify everything in one go:

ssh -i /path/to/pem-key-1 ubuntu@172.31.24.63 << 'EOF'
echo "=== Agent Setup Verification ==="
echo "✓ SSH connection successful"
echo "Java version: $(java -version 2>&1 | head -1)"
echo "Working directory: $(pwd)"
echo "Jenkins agent directory:"
ls -la ~/jenkins-agent
echo "Authorized keys:"
grep -c 'ssh-rsa' ~/.ssh/authorized_keys
echo "Disk space:"
df -h /home/ubuntu | tail -1
echo "✓ All checks passed!"
EOF

If this completes successfully, your setup is complete.

================================================================================

That covers all 7 steps in detail. Reference this guide as you go through each step.
