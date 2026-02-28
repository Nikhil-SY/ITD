================================================================================
STEP-BY-STEP: ADD JENKINS AGENT VIA SSH WITH PRIVATE KEY
================================================================================

SCENARIO:
  - Jenkins Controller: Running on main server
  - Jenkins Agent: Remote machine at 172.31.24.63 (private IP)
  - Authentication: RSA private key (pem-key-1)
  - Remote user: ubuntu
  - SSH Port: 22

================================================================================
PREREQUISITES
================================================================================

Before starting, ensure you have:

1. ✓ Jenkins is installed and running on the controller
2. ✓ Jenkins plugins installed:
     - SSH Slaves Plugin (ssh-slaves)
     - SSH Credentials Plugin (ssh-credentials)
     - Trilead API Plugin (trilead-api)
   
   To install: Manage Jenkins > Manage Plugins > Available tab > Search for "ssh"

3. ✓ Remote machine (172.31.24.63) has:
     - SSH server running
     - Java installed (same version as Jenkins controller)
     - SSH key-based authentication enabled
     - Ubuntu user account with sudo access
     - Sufficient disk space (~2-5 GB)

4. ✓ Network connectivity:
     - Jenkins controller can reach 172.31.24.63 on port 22
     - No firewall blocking SSH (port 22)
     - No NAT/routing issues

================================================================================
STEP 1: PREPARE THE REMOTE MACHINE (172.31.24.63)
================================================================================

Connect to the remote machine (however you normally do):
  ssh ubuntu@172.31.24.63

Then run these commands:

1.1 Install Java (if not already installed)
  sudo apt update
  sudo apt install -y openjdk-17-jre-headless
  java -version  # Verify installation

1.2 Create jenkins user (if you want to run agent as jenkins user)
  sudo useradd -m -s /bin/bash jenkins
  sudo usermod -aG sudo jenkins  # Optional, if jenkins needs sudo

1.3 Create .ssh directory for the user who will run Jenkins agent
  
  # If using 'ubuntu' user:
  mkdir -p ~/.ssh
  chmod 700 ~/.ssh
  
  # If using 'jenkins' user:
  sudo mkdir -p /home/jenkins/.ssh
  sudo chmod 700 /home/jenkins/.ssh
  sudo chown jenkins:jenkins /home/jenkins/.ssh

1.4 Add your public key to authorized_keys
  
  # Extract public key from your RSA private key:
  ssh-keygen -y -f pem-key-1 > pem-key-1.pub
  
  # On the remote machine, add it to authorized_keys:
  cat >> ~/.ssh/authorized_keys << 'EOF'
  [PASTE THE CONTENTS OF pem-key-1.pub HERE]
  EOF
  
  chmod 600 ~/.ssh/authorized_keys

1.5 Create Jenkins agent working directory
  mkdir -p ~/jenkins-agent
  chmod 700 ~/jenkins-agent

1.6 Test SSH connection from Jenkins controller
  ssh -i pem-key-1 -v ubuntu@172.31.24.63
  
  Should succeed without password prompt.
  Type 'exit' to close connection.

================================================================================
STEP 2: ADD SSH CREDENTIALS IN JENKINS
================================================================================

2.1 Go to Jenkins Dashboard
  - Open your Jenkins URL (e.g., http://localhost:8080)
  - Click "Manage Jenkins" in left sidebar

2.2 Navigate to Credentials
  - Click "Manage Jenkins"
  - Click "Manage Credentials" (or go directly: /credentials)

2.3 Select the appropriate store and domain
  - Click on "System" > "Global credentials (unrestricted)"

2.4 Create new SSH key credential
  - Click "Add Credentials" button (top-left)

2.5 Fill in the credential details
  Kind:                    "SSH Username with private key"
  Scope:                   "Global (Jenkins, nodes, items, all child items, etc)"
  ID:                      "pem-key-1" (or your preferred ID)
  Description:             "EC2 Agent SSH Key for 172.31.24.63"
  Username:                "ubuntu"
  Private Key:             ○ Enter directly
  
  [CLICK ON "Enter directly" RADIO BUTTON]
  
2.6 Paste your private key
  - Copy the ENTIRE content of your pem-key-1 file (including BEGIN and END)
  - Paste it in the "Private Key" text area:
  
    -----BEGIN RSA PRIVATE KEY-----
    MIIEpAIBAAKCAQEA...
    [rest of key content]
    -----END RSA PRIVATE KEY-----

2.7 Handle passphrase (if key is encrypted)
  Passphrase:             [LEAVE EMPTY if unencrypted]
                          [OR ENTER THE PASSWORD if encrypted]

2.8 Save the credential
  - Click "Create" button
  - You should see the credential listed now

================================================================================
STEP 3: CREATE NEW JENKINS AGENT NODE
================================================================================

3.1 Go to Node Management
  - Click "Manage Jenkins" in left sidebar
  - Click "Manage Nodes and Clouds"

3.2 Create new node
  - Click "New Node" button (or "Create a new node")
  - Enter Node name: "agent-172-31-24-63" (or your preferred name)
  - Select: "Permanent Agent"
  - Click "Create"

3.3 Configure node properties
  
  Number of executors:           2
                                 (or match number of CPU cores)
  
  Remote root directory:         /home/ubuntu/jenkins-agent
  
  Labels:                        agent docker linux
                                 (add labels for targeting builds)
  
  Usage:                         "Use this node as much as possible"
  
  Launch method:                 ○ Select "Launch agents via SSH"

3.4 Configure SSH settings
  Host:                          172.31.24.63
  
  Credentials:                   Select "pem-key-1" from dropdown
                                 (the credential you just created)
  
  Host Key Verification          "Non verifying Verification Strategy"
  Strategy:                       (NOT recommended for production, but works)
  
  Or select:                      "Known hosts file Verification Strategy"
                                 (requires setting up known_hosts)
  
  SSH Key Connection Timeout:    60 seconds
  
  Max number of retries:         10
  
  Retry wait time:               15 seconds

3.5 Configure node availability (optional)
  
  Availability:                  "Keep this agent online as much as possible"

3.6 Configure tool locations (optional)
  
  JVM options:                   [LEAVE EMPTY or add: -Xmx1024m]
  
  Java Path:                     [LEAVE EMPTY - auto-detect]
  
  Prefix Start Agent Command:    [LEAVE EMPTY]
  
  Suffix Start Agent Command:    [LEAVE EMPTY]

3.7 Save configuration
  - Scroll to bottom and click "Save"

================================================================================
STEP 4: START THE AGENT
================================================================================

4.1 Go back to "Manage Nodes and Clouds"
  - You should see your new node listed

4.2 Click on your node (e.g., "agent-172-31-24-63")

4.3 Click "Relaunch agent" or wait for auto-launch
  - Jenkins will attempt to SSH into 172.31.24.63
  - Java will be started on the remote machine
  - Agent should connect back to Jenkins

4.4 Monitor the log
  - You should see a log window showing connection progress
  - Look for messages like:
    ✓ [SSH] Opening SSH connection to 172.31.24.63:22
    ✓ [SSH] Authentication successful
    ✓ Agent successfully connected and online

4.5 Verify agent is online
  - Look at the "Manage Nodes" page
  - Your node should show a green circle (online)
  - If red circle, scroll down to see error logs

================================================================================
STEP 5: TEST THE AGENT
================================================================================

5.1 Create a test job
  - Click "New Item" in Jenkins dashboard
  - Enter job name: "Test-Agent"
  - Select "Freestyle job"
  - Click "OK"

5.2 Configure job to use the agent
  Under "General" section:
  ☑ Restrict where this project can be run
  Label Expression:  "agent" (or whatever label you assigned)

5.3 Add a build step
  Under "Build" section:
  - Click "Add build step"
  - Select "Execute shell"
  - Enter commands:
    
    echo "Testing Jenkins Agent"
    hostname
    pwd
    java -version
    whoami

5.4 Save and run the job
  - Click "Save"
  - Click "Build Now"
  - Click on the build number to see console output

5.5 Verify success
  - Should see output from the remote machine (hostname, pwd, etc.)
  - If it runs on controller instead, check agent connectivity

================================================================================
STEP 6: TROUBLESHOOTING
================================================================================

Issue: Agent shows as OFFLINE (red circle)
------------------------------------------
1. Click on the node name
2. Scroll down to see the error log
3. Common errors and solutions:

   A) "Authentication failed" or "Publickey authentication failed"
      ✓ Verify the RSA key format (openssl rsa -in pem-key-1 -check -noout)
      ✓ Check if key is encrypted and try decrypting it
      ✓ Verify key is in authorized_keys on remote machine
      ✓ Check passphrase is correct in Jenkins credential
   
   B) "Permission denied (publickey,password)"
      ✓ SSH key not in authorized_keys on remote machine
      ✓ Run on remote: cat ~/.ssh/authorized_keys
      ✓ If empty, add your public key again
   
   C) "java.io.IOException: PEM problem: it is of unknown type"
      ✓ Key format is wrong (use RSA, not OpenSSH format)
      ✓ Try: ssh-keygen -p -m pem -f pem-key-1
      ✓ Re-upload the key to Jenkins credentials
   
   D) "Remote host is not running Java"
      ✓ Install Java on remote: sudo apt install -y openjdk-17-jre-headless
      ✓ Verify: ssh ubuntu@172.31.24.63 "java -version"
   
   E) "Connection timeout" or "Cannot reach host"
      ✓ Check network connectivity: ping 172.31.24.63
      ✓ Check SSH is running on remote: sudo systemctl status ssh
      ✓ Check firewall: sudo ufw allow 22/tcp
      ✓ Check security groups (if AWS): allow inbound SSH from Jenkins controller IP

Issue: Agent connects but builds don't run on it
-------------------------------------------------
✓ Verify job has correct label in "Restrict where this project can be run"
✓ Check agent has non-zero executors (set in node configuration)
✓ Restart the agent: Go to node > Relaunch agent

Issue: Agent disconnects randomly
---------------------------------
✓ Increase SSH timeout in node configuration
✓ Add to Jenkins system properties: -DclientKeepAliveInterval=30
✓ Check remote machine resources (disk space, memory, CPU)
✓ Check for network issues or firewall rules resetting connections

================================================================================
STEP 7: VERIFY EVERYTHING (FINAL CHECKLIST)
================================================================================

Before considering this complete, verify:

☑ Jenkins can SSH into 172.31.24.63 without password
☑ Credential "pem-key-1" is created and visible in Jenkins
☑ Node "agent-172-31-24-63" is created
☑ Node shows as "Online" (green circle)
☑ Test job runs successfully on the agent
☑ Agent shows in node description
☑ Label "agent" is properly assigned and working
☑ Java is installed on remote machine
☑ Jenkins-agent directory exists on remote machine
☑ SSH key is in authorized_keys on remote machine

================================================================================
OPTIONAL: SET UP KNOWN_HOSTS VERIFICATION (PRODUCTION RECOMMENDED)
================================================================================

For production, use "Known hosts file Verification Strategy" instead of
"Non verifying Verification Strategy".

1. On Jenkins controller, add the remote host to known_hosts:
   ssh-keyscan -t rsa 172.31.24.63 >> ~/.ssh/known_hosts
   
   (Or if Jenkins runs as different user)
   sudo -u jenkins ssh-keyscan -t rsa 172.31.24.63 >> /home/jenkins/.ssh/known_hosts

2. In Jenkins node configuration, change to:
   Host Key Verification Strategy: "Known hosts file Verification Strategy"

3. Specify the known_hosts file location (Jenkins will auto-find it)

================================================================================
OPTIONAL: EXECUTE INIT SCRIPT WHEN AGENT STARTS
================================================================================

If you need to run commands when the agent starts:

1. In node configuration, add to:
   "Prefix Start Agent Command"
   
   Example:
   export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

2. Or add to:
   "Suffix Start Agent Command"
   
   Example:
   && source ~/.bashrc

================================================================================
QUICK REFERENCE: KEY JENKINS AGENT SSH SETTINGS
================================================================================

Remote Host:              172.31.24.63
Remote User:              ubuntu
SSH Credentials:          pem-key-1 (SSH key credential)
Remote Root Directory:    /home/ubuntu/jenkins-agent
SSH Port:                 22 (default)
Connection Timeout:       60 seconds
Max Retries:              10
Retry Wait Time:          15 seconds
Host Key Verification:    NonVerifyingKeyVerificationStrategy
Launch Method:            SSH Launcher
TCP No Delay:             true

================================================================================
