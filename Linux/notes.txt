BareMetal - OS is installed directly on hardware, no Hypervisor in between, high performance compared to virtual server

AWS uses HVM[Hardware virtual machine] virtualization, it uses AWS Nitro [nvme], previously it was using Xen [xvda] 

semver.org -> To  know about versioning 20.01.6

versions we are using:
Ubuntu - 24.04

To print content
cat demo.txt
sed '' demo.txt
sed -n 'p' demo.txt
awk '{print}' demo.txt

Linux:


Day 1: on-prem, Cloud
SELinux (Security-Enhanced Linux) is a powerful security module in the Linux kernel that enforces Mandatory Access Control (MAC) policies, adding a crucial layer beyond standard Linux permissions (DAC) to confine processes and users.
On-Premises (On-Prem)
•	On-prem is when your servers and infrastructure are physically located in your organization’s own datacenter (company owned buildings).
•	Company is responsible for everything — hardware, networking, power, cooling, admins and security.
•	It gives full control but requires heavy capital cost and maintenance.
Server
•	A server is just a machine/computer or software system that provides services or resources to other computers or clients over a network.
•	In today’s context, it could be a Virtual Machine, or even a cloud instance like an EC2
example: Web Server, Application Server, Database Server, File Server, Mail Server, Game Server etc.
Physical server → A real hardware machine.
Virtual server → A software-based server running inside a VM or container.
Bare Metal
Bare metal refers to running workloads directly on physical hardware, without any hypervisor or virtualization layer in between.
You get 100% of the machine’s CPU, memory, storage, and network, exactly as the hardware provides it.
Unlike virtual machines, there is no resource sharing, no noisy neighbors, and no hypervisor overhead.
Key Characteristics
•	Direct hardware access – OS runs straight on the server
•	Highest performance & lowest latency
•	Full control over BIOS, firmware, kernel tuning, CPU pinning, NUMA
•	Predictable performance (critical for real-time systems)
•	Manual scaling compared to cloud VMs
Cloud
•	Cloud is basically someone else’s computer — but with industrial-grade scalability and automation.
•	You don’t buy hardware; instead, you rent servers, storage, databases, and more on demand.
•	It lets you focus on your application or service, while the provider takes care of the messy infrastructure — power, cooling, networking, redundancy, the whole lot.
•	It evolved from traditional datacenters to offer agility — spin up 100 servers in minutes, pay-as-you-go, and scale down when you don’t need them. It’s not just cost savings — it’s about speed, flexibility, and global reach.
Public Cloud
•	Public cloud is what most people refer to when they say ‘cloud’ — platforms like AWS, Azure, or GCP.
•	The infrastructure is owned and managed by the provider, and you’re just renting what you need — compute, storage, databases, etc.
•	It’s cost-efficient, globally available, and highly scalable, but you share physical resources with others.
Private Cloud
•	Private cloud gives you cloud-like flexibility, but the infrastructure is dedicated to your organization — either on-prem or hosted by a third party.
•	Tools like OpenStack or VMware help you build it. It’s ideal for security-sensitive workloads, compliance, or when you need more control over your environment.
In-House
In-house usually refers to custom-built software or infrastructure managed by your own team, regardless of where it’s hosted. For example, even on cloud, if your team builds and manages everything end-to-end, that’s in-house expertise. 



Day 2:  Introduction
Ubuntu
Most Popular for devs, cloud, and general use.
 
Red Hat Enterprise Linux (RHEL)
Enterprise-grade OS — stable, long support cycles.
 
CentOS
Upstream of RHEL. Used for testing RHEL-like environments.
 
Debian
Very stable, used in backend servers, cloud VMs.
 
Amazon Linux
Optimized for AWS (fast boot, tuned kernel).
 
Overall 
 
Operating System Usage on Servers (2025) — Industry Estimate
 

Day 3:  Connect to Remote EC2 (SSH)
Create an ec2 instance (Server, Virtual Machine, Node)
Step-by-Step Guide to Create an EC2 Instance
1.	Log in to AWS Management Console:
•	Go to the AWS Management Console and log in with your credentials.
2.	Navigate to EC2:
•	In the AWS Management Console, search for “EC2” in the services search bar and select it.
3.	Launch Instance:
•	Click on the “Launch Instance” button.
4.	Choose an Amazon Machine Image (AMI):
•	Select an AMI that suits your needs (e.g., Amazon Linux, Ubuntu, RHEL). You can choose from free-tier eligible options if you're just getting started.
5.	Choose an Instance Type:
•	Select the instance type (e.g., t2.micro for free tier). Click “Next: Configure Instance Details” after making your selection.
6.	Configure Instance Details:
•	Set the number of instances, network settings, and other details. For a simple setup, the default settings are usually sufficient. Click “Next: Add Storage.”
7.	Add Storage:
•	Modify the storage size if necessary. The default is typically sufficient, but you can add more if needed. Click “Next: Add Tags.”
8.	Review and Launch:
•	Review your instance configuration. Click “Launch.”
9.	Select or Create a Key Pair:
•	If you don’t have a key pair, create a new one and download it (keep it safe; you won't be able to download it again). If you have one, select it. Click “Launch Instances.”
10.	View Instances:
•	Click on “View Instances” to see your new EC2 instance. It may take a few minutes to initialize.
Accessing Your EC2 Instance
•	For Linux Instances:
•	Use SSH to connect. The command will look like this:
ssh -i /path/to/your-key.pem <username>@<your-ec2-public-ip>
For an Amazon Linux AMI, the username is ec2-user.
For a CentOS AMI, the username is centos or ec2-user.
For a Debian AMI, the username is admin.
For a Fedora AMI, the username is fedora or ec2-user.
For a RHEL AMI, the username is ec2-user or root.
For a SUSE AMI, the username is ec2-user or root.
For an Ubuntu AMI, the username is ubuntu.
For an Oracle AMI, the username is ec2-user.
For a Bitnami AMI, the username is bitnami.
Preffered SSH client: 
•	git bash Download
•	Mobaxterm Download
Day 4:  pwd, ls, tree, rm, mkdir, touch
Linux keynotes to know 
•	In Linux commands are case-sensitive (all commands are in lowercase)
•	A folder is called a Directory in Linux
•	Everything is a file in Linux, including directories, devices, and processes.
•	The root user (root) has full administrative privileges.
•	/ (root directory) is the top-level directory in the Linux filesystem.
•	Hidden files start with a dot (.), e.g., .bashrc.
•	Use man followed by a command (e.g., man ls) to see the manual page.
Unix tradition: Almost all commands follow lowercase due to Unix/Linux history and POSIX standards.
Case-sensitive in Linux: Linux treats ls and LS as different. Only ls exists, so LS gives “command not found”.
Simplicity & consistency: Lowercase keeps commands predictable and easy to type.
 
Convention	Description
-<letter>	Short option; typically 1 letter, often stackable (e.g., -xzvf)
--<word>	Long option; more readable, not usually combinable
= for long options	Long options often allow assignment (--output=file.txt)
Use --help	Most commands support --help to print usage
Option order matters	Sometimes, positional arguments matter after options
 
man command (manual)
 
man <command>
man ls
 
Common keys when reading man:
• 🔼 / 🔽 – Scroll up/down
• /<keyword> – Search for a word
• n – Next match
• q – Quit
 
pwd
The pwd command stands for "print working directory."
It prints the path of the working directory. 
$ pwd
/home/ubuntu
 
ls (list files and directories)
•	To list with details (long format): ls -l
•	To list with creation time sorted (recent at the top): ls -t
•	To list reverse order: ls -r
•	All the above together: ls -lrt (OR) ll
rm - Delete files/directories
Use the rm command to delete files and directories. But rm cannot simply delete a directory. Use “rm -r” to delete a directory. In this case, it deletes both the folder and the files in it.
    To remove/delete a file     
        rm file_name 
    To remove/delete a Directory    
        rm -r directory

cd (change directory - cd)
•	switch/change to a folder/Directory in Linux
   Syntax: cd <path>/<location>
   example: 1. To change to a Directory in the current location
                        cd test
mkdir (make directory - mkdir)
•	To create a directory: mkdir <directory_name>
           example: mkdir test
•	To create multiple directories:
      mkdir <directory_name> <directory_name1> <directory_name2> ..... <directory_name>
           note: directory names with space separated    
           example: mkdir test test1 test2 ...   
tree 
Inastall tree 
#Before installing any software/tools, refresh the package list to get the latest package
sudo apt update

#Once the package list is updated, install the desired software using apt
sudo apt install tree
The tree command in Linux is used to display the contents of current directory in a tree-like format. It recursively lists all files and directories within a specified directory.
 
1.	Display Only Directories: tree -d
2.	List All Files Including Hidden Files: tree -a
3.	Limit the Depth of the Tree: tree -L 2
4.	Display Full Path Prefix for Each File: tree -f 
5.	Print the Size of Each File: tree -h
touch
touch is used to create empty files or update file timestamps (access & modification time).

#Create a new empty file
       touch file.txt

#Create multiple files
       touch a.txt b.txt c.txt

#Update timestamp of an existing file
       touch file.txt

#Create file with full path
       touch /home/ubuntu/test.log


Day 5:  cp (copy), mv (move/rename)
cp - Copy the file from one location to another 
cp command copies files and directories through the command line. 
cp [OPTIONS] <SOURCE> <DESTINATION>
 
To copy to a different location
cp file1.txt /home/ubuntu/Dir1
To copy file and rename
cp file1.txt file2.txt
Copy a directory recursively
cp -r dir1/ dir2/
Copy multiple files to  directory
cp file1.txt file2.txt file3.txt file4.txt /home/user/Dir1/
Ask before overriting file (Prompt y/n)
cp -i file1.txt /home/user/Dir1/
copy file without changing timestamp and permissions
cp -p file.txt  /home/user/Dir1/

mv - Rename or Move the file from one location to another

rename or move the file from one location to another (mv)

•	mv command to move files and directories through the command line.
•	We can also use the mv command to rename a file/directory.
    To rename a file/directory
        mv old_filename new_filename
        mv old_directory new_directory
    To move to a different location (cut and paste)    
        mv <source> <destination>


Day 6: free, top, htop, lscpu, uptime, ps, hostnamectl

cat /etc/os-release
•	Prints details of the Linux distribution in a simple KEY=VALUE format.
•	Common fields include the OS name, version, and ID, which scripts often parse to detect the distro.
 
hostnamectl
Displays and lets you set hostname plus OS details on systemd systems.
 
free
Free command is used to check the used and available space of physical memory and swap memory (ram/memory) in KB. The free command displays:
• Total amount of free and used physical memory
• Total amount of swap memory in the system
• Buffers and caches used by the kernel
/proc/meminfo
cat /proc/meminfo will contain dynamic information about the kernel and the system.
 
top
The top command also gives you a real-time update on how much of your swap space is being used.
 
htop
Improved version of top with colors, bars and easier navigation.
 
uname
uname command displays important information about the system such as — Kernel name, Host name, Kernel release number, Processor type, etc.,
     To Displays all available system information in a single line
        uname -a
    To check the linux version 
        uname -a (or) cat /etc/os-release (or) lsb_release -a 
 
$ uname -a
Linux hostname 5.4.0-42-generic #46-Ubuntu SMP Fri Sep 18 16:21:19 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 
uptime
The uptime command in Linux provides information about how long the system has been running, along with other statistics related to system load
 
$ uptime
14:35:29 up 10 days,  3:12,  2 users,  load average: 0.10, 0.15, 0.20
Breakdown of the Output:
•	Current time: 14:35:29 (the time when the command was run).
•	Uptime: up 10 days, 3:12 (indicates the system has been running for 10 days and 3 hours).
•	Number of users: 2 users (the number of users currently logged into the system).
•	Load average: load average: 0.10, 0.15, 0.20 (the average number of processes in the run queue over the last 1, 5, and 15 minutes).
lscpu
The lscpu command in Linux displays detailed CPU architecture information. It fetches this from /proc/cpuinfo and sysfs.
 
Swap Info
swapon --show


Day 7: df, ifconfig, ip, Load Average
df - Disk Free (filesystem view)
•	The command df stands for "Disk Free" or some refer as "Disk Filesystem".
•	With the -h option (df -h) it shows the disk space in "human readable" form.
•	df shows total, used, and available space at the filesystem level (mount points).
•	First command to run when app says “No space left on device”
df -h
Load Average 
•	Load average is the average number of processes that are either running on CPU or waiting for mainly CPU.
•	It tells how busy your system is, not just CPU usage also disk I/O but mainly we use this value to know CPU usage.
•	uptime
•	top
htop
Ideal Load ≈ Number of CPU cores
Example: load average: 0.72, 1.10, 1.45
  For 4-core EC2 Virtual Machine 
•	Healthy system Load Average (CPU is underutilized): 1.2
•	Busy system Load Average (System is busy but manageable): 3.8
•	Overloaded system Load Average (Processes are waiting → slow apps): 7.5
ifconfig (Old / legacy command)
•	ifconfig is the traditional network interface configuration command used in older Linux systems.
•	ifconfig is deprecated and replaced by the ip command in modern Linux.
What it shows
• Interface name (eth0, ens5, lo)
• Private IP
• MAC address
• RX/TX packets
 
ip command (Modern & recommended)
•	ip command shows interfaces & IPs and is preferred because its Faster, More features, Actively maintained, Works with namespaces, containers, cloud networking.
•	ip addr 
ip addr show
 
Note: Public IP will NOT show in ifconfig or ip addr Because AWS NATs (Network Address Translation) it outside the instance.
1.	Correct way to get public IP of ec2 (AWS Metadata service)
curl http://169.254.169.254/latest/meta-data/public-ipv4
Note: Only accessible from inside the EC2 and Secure, no internet needed.
2.	AWS-hosted public IP check application service

curl https://checkip.amazonaws.com/
 
3.	Calling Public IP lookup service 
curl ifconfig.me
•	Calls a public website which replies with your public IP.
•	Requires outgoing internet access for ec2 machine. 
•	This command will not work if ec2 machine is in private subnet network without Internet gateway. 
•	Basically It show the Public IP of ec2 machine as seen by the internet.
EC2 → Internet → ifconfig.me → returns IP
There are many other public IP echo services same as  ifconfig.me or checkip.amazonaws.com

curl ipinfo.io/ip
curl icanhazip.com
curl api.ipify.org
curl ident.me


Day 8: wget, curl, ports
wget
•	wget is a command-line utility used to retrieve files from the web using HTTP, HTTPS, and FTP protocols.
•	wget is another popular command-line tool used to download files from the web.
•	wget is similar to curl, but it’s specifically designed for downloading files.
•	wget is often preferred for batch downloads or recursive downloading.
To download a file from a URL:
wget https://example.com/file.zip
Download and save with a custom filename:
wget -O custom_filename.zip https://example.com/file.zip
Download a website recursively (e.g., all pages and media):
wget -r https://example.com
Download a file in the background:
wget -b https://example.com/file.zip
 
curl
•	curl is used to access a website and retrieve its content
•	curl is a command-line tool used for transferring data to or from a server, and it supports multiple protocols such as HTTP, HTTPS, FTP, and more.
curl https://example.com

#Show headers only (no content):
curl -I https://example.com

#To get only status code 
curl -s -o /dev/null -w "%{http_code}" https://example.com
Port
A port is a logical endpoint in a network communication used to identify specific processes or services running on a server. When data is transmitted over a network, it is sent to a specific IP address and a port number to reach the correct service/Applicaiton running on the destination server.
 


Day 9: VI Editor, echo, > Redirect, >> Append, | (pipe), &&, ||, ;

Vi Editor 
Command Mode 
•	we can't add any content. This is used to run vi-related commands.
•	Initially when we do vi to a file command mode is the default mode.
    Basic File Operations
•	
•	Save changes to the file: :w
•	Quit without saving: :q!
•	Save and quit: :wq! or <Esc> then Shift + ZZ
•	Save to another file: :w <new_file>
     Navigation & Editing
•	
•	Undo last change: u
•	Redo last undone change: Ctrl + r
•	Search for a word: /<word>
•	Display line numbers: :set nu
•	Disable line numbers: :set nu!
•	Replace a word globally: :s/<old_word>/<new_word>/g
     Cut, Copy, and Paste
•	
•	Cut the current line: dd
•	Copy the current line: yy
•	Paste the copied/cut content: p
•	Delete a word: dw
•	Delete to the end of the line: D
•	Delete from the cursor to the end of the file: dG
Insert Mode
•	Is used to add the content to the file.
•	Press 'i' to enter to insert mode 
•	Press '<escape>' to exit insert mode and move to command mode.
echo 
The echo command is used to display a message or output a string to the terminal.
echo "Hello, World!"
> (Write to a File using the Redirection Operator) 
•	Redirection allows you to capture the output from a command and overwrite it as input to another command or file.
•	It will overwrite/Erase all the content of a file and add new content to the file.
•	Whatever the content it will written to a file and nothing will be printed in the console.    
•	#This is Redirection of text to file
•	echo "This is Redirection of text to file" > file.txt
•	
•	#Redirect any command output to file 
ls -lrt > file.txt
Empty file content in Linux without deleting the file
> <filename>
 
>> (Append to a File using the double Redirection Operator)
 
•	Double Redirection allows you to capture the output from a command and send it as input to another command or file.
•	It will append the content to the end of the file by keeping the old content.
#Append text to end of file
echo "This is Redirection of text to file" >> file.txt

#Append any command output to end of file 
ls -lrt >> file.txt
Semicolon (;)
•	The semicolon operator executes commands sequentially, regardless of the success or failure of preceding commands.
<COMMAND1>; <COMMAND2>; <COMMANDn>
 
&& - Logical AND
•	The ‘&&’ command in Bash is a logical operator that allows you to execute multiple commands in sequence.
•	The next command in the sequence will only execute if the previous command has been executed successfully (returns an exit status of 0).
•	command_1 && command_2
•	
•	#Create Directory and CD to the directory 
•	mkdir new_folder && cd new_folder
•	
•	#Update and install packages
sudo apt update && sudo apt install <packages/tools>
 
||
The ‘||’ command in Bash is a logical OR operator. It will execute the next command only if the previous command fails.
 
command_1 || command_2
 
| (pipe)
 
•	The output of one command can given as input to another command
•	The Unix/Linux systems allow the stdout of a command to be connected to the stdin of another command. 
•	The pipe is used to combine two or more commands, and in this, the output of one command acts as input to another command
command_1 | command_2 | command_3 | .... | command_N
Real-world examples of using the | with xargs
1.	Counting the Number of Files in a Directory

find . -type f | wc -l
2.	Finding and Counting Specific Files
find . -type f -name "*.txt" | wc -l
3.	Removing Files with a Specific Extension (file type)
find /path/to/directory -type f -name "*.log" | xargs rm
4.	Find process is running or not
ps -ef | grep <process_name>
5.	Renaming Files Using mv
ls *.txt | xargs -I {} mv {} {}.bak
6.	Copying .conf Files to a Backup Directory
find /etc -type f -name "*.conf" | xargs -I {} cp {} /backup_path


Day 10: grep
grep (To search pattern/string in a file or content)
grep ‘global search for the regular expression’:
•	By default, grep searches line by line in a file and prints only the matching lines.
o	grep "linux" file.txt
•	By default, grep searches are case-sensitive. Use -i option is used to ignore case.
o	grep -i "linux" file.txt
•	By default, grep searches for a pattern anywhere in a line (substring). Use -w to match whole words only.
o	grep "the" file.txt   # Matches "the", "there", "their", etc.  
o	grep -w "the" file.txt  # Matches only "the", not "there" or "their".
•	grep supports basic regular expressions (BRE) by default. use -E enables extended regular expressions (ERE) (same as egrep).
Using Pattern and Regex
1) Match all lines that start with -> 
     grep “^hello” file1


2) Match all lines that end with  -> 
     grep “done$” file1


3) Match all lines that contain any of the letters ‘a’,‘b’,‘c’,‘d’or‘e’ -> 
     grep “[a-e]” file1


4) Match all lines that start with a vowel -> 
     grep “^[aeiou]” file1


5) Match all lines that start with a digit following zero or more spaces. E.g:“1.”or“2.” -> 
     grep “ *[0-9]” file1
     1. Finds any 3-digit sequence, like 123, 456, etc.
         grep "[0-9][0-9][0-9]" file.txt
 
6) Match a Basic 10-Digit Indian Mobile Number
    grep -E "\b[6789][0-9]{9}\b" file.txt
 
•	By default grep searches single pattern. Use -e option for Multiple Patterns
o	grep -e "pattern" -e "pattern"
•	By default, grep can search inside directories recursively. 
o	grep -r "linux" *
Searching in all files recursively in a directory.
1) Search for a Word in All Files Recursively in directory
    grep -r "error" /var/log/
 
2) Case-Insensitive Recursive Search
    grep -ri "error" /var/log/
 
3) Searches only in Python files.
    grep -r "text" --include="*.py"
 
4) Excludes .log files.
    grep -r "text" --exclude="*.log"
 
•	Use -o to extract and print matching portions only (not print full lines).
o	# Print only phone numbers not complete line containing phone number.  
o	grep -o "[0-9]\{10\}" contacts.txt  
•	grep can show line numbers of matches.
o	#Shows all lines containing "linux" with line numbers.  
o	 grep -n "linux" file.txt 
Day 11: sed

sed
SED command in UNIX stands for stream editor and it can perform lots of functions on file like searching, finding and replacing, insertion or deletion. 
 
•	To replace all occurrences in each line, add the global (g) flag:
sed 's/old_text/new_text/g' filename
•	in-place editing (modifying the file directly):

sed -i 's/old_text/new_text/g' filename
•	Case-Insensitive Substitution

sed 's/old_text/new_text/I' filename
•	Apply multiple substitutions using the -e option:

sed -e 's/old_text1/new_text1/' -e 's/old_text2/new_text2/' filename
•	Remove all blank lines from a file:
sed '/^$/d' filename
Consider the following text file as the input file for all cases below. (file.txt)
Unix is a great os. Unix is open source. Unix is a free os.
learn operating systems.
Unix Linux which one you choose.
Unix is easy to learn. Unix is a multiuser os. Learn unix .unix is a powerful.
 
Some common interview related examples 
    1) Replacing or substituting string
sed 's/unix/linux/' file.txt
    2) Replacing the nth occurrence of a pattern in a line 
sed 's/unix/linux/2' file.txt
    3) Replacing all the occurrences of the pattern in a line
sed 's/unix/linux/g' file.txt
    4) Replacing from nth occurrence to all occurrences in a line
sed 's/unix/linux/3g' file.txt
    5) Replacing string on a specific line number
sed '3s/unix/linux/g' file.txt
    6) Printing only the replaced lines
sed -n 's/unix/linux/p' file.txt
    7) Deleting lines from a particular file
To Delete a particular line, say 5 in this example
sed '5d' file.txt
To Delete a last line
sed '$d' file.txt
To Delete line from range x to y            
sed '3,6d' file.txt
       To Delete from the nth to the last line
sed '12,$d' file.txt
       To Delete pattern-matching line
sed '/pattern/d' file.txt
To delete lines in a file that contain a specific string:
sed '/pattern/d' filename


    8) Print a specific line from a file
sed -n '2p' file.txt
    9) Insert and Append Text
•	
•	Insert text before a specific line (e.g., before line 2):

sed '2i\This is the inserted line.' file.txt
•	Append text after a specific line (e.g., after line 2):
sed '2a\This is the appended line.' file.txt

Day 12: find
find
find command can be used to find files and directories and perform subsequent operations on them. It supports searching by file, folder, name, creation date, modification date, owner and permissions. By using the ‘-exec’ other commands can be executed on files or folders found.
 
SYNTAX: find <location_to_find> [options]
 
combine multiple conditions in a find command
find . -name "*.txt" -and -mtime -7
 
To search for multiple filenames using the find command
1.	You can combine multiple -name options with the -o (logical OR) operator
2.	find . -name "file1.txt" -o -name "file2.txt"
find . -name "file*" -o -name "new*"
3.	Using -regex
find . -regex '.*\(file1\.txt\|file2\.txt\)'
Some common interview related examples 
1) Search file with specific name
find . -name file.txt
   
2) Search file with specific name with ignorecase  
find . -iname file.txt
   
3) search files in multiple directories
 find . /home /user -name file.txt
    
4) Search only files containing name
find . -type f -iname file.txt
   
5) Search only directories containing name     
find . -type d -iname file.txt
   
6) Search for empty files and directories
find . -empty
   
7) Search for file with permissions(655)     
find . -perm 655
   
8) Search text within multiple files.      
 find./-typef-name"*.txt"-execgrep'search_string' {}\;
   
9) find files by last modification time
find . -mtime days
       # 24 hours 
find . -mtime 1
       # modified less than 7 days (7 days to till) 
find . -mtime -7
       # Last 50-100 Days Modified Files
find . -mtime +50 –mtime -100 
   
10) Find Last 50 Days Accessed Files
find . -atime 50
   
11) Find Changed Files in Last 1 Hour
find / -cmin -60
 
12) Find Accessed Files in Last 1 Hour
find / -amin -60
 
13) Find files larger than a specific size 
find . -size +100M
 
14) Find modified on a specific date 
find /path/to/directory -type f -newermt 'YYYY-MM-DD'
find . -type f -newermt '2025-02-20'
15) Find files owned by a specific user
find . -user username
ex: find . -user ubuntu

Day 13: root, superuser, su, sudo, chmod
Root User (UID 0)
•	The root account is the superuser
•	Has UID = 0
•	Has unrestricted system access
Root should be used rarely — to avoid accidental system damage.
 
Root can:
•	read/write any file
•	kill any process
•	install/remove software
•	change ownership & permissions
•	modify kernel/security configs
System Users (Non-login Service Accounts) (UID 1 - 999)
System users are created for system services & daemons
•	They do not have passwords
•	They cannot log in interactively
•	They are used to run background processes securely
Login users (Interactive Users) (UID 1000+)
On Ubuntu & most modern Linux:
•	First login user starts at UID 1000
•	Created during OS install
/etc/sudoers
Granting Controlled Admin Access
The sudoers file defines:
•	who can run admin commands
•	with or without password
•	which hosts/commands are allowed
sudo visudo  OR  sudo vi /etc/sudoers
Give a user sudo access
Method_1: Add the below line in /etc/sudoers
<username> ALL=(ALL:ALL) ALL
 
Method_2: Add the user to sudo group 
sudo usermod -aG sudo <username>
sudo  
Run Single Command With Admin Privileges
sudo apt update
 
Check current user groups
groups
Check another user:
groups <username>
su — Switch User Account
sudo su - <username>
switch to root 
sudo su -    OR   sudo su - root 
 
chmod 
•	The chmod command is used to change the access mode of a file. 
•	The name is an abbreviation of change mode. 
 
 
   example: 1. Read, write and execute permissions to the file owner: 
                             chmod u+rwx <file_name>
                                             (OR)
                             chmod 700 <file_name>
                   2. Read, write to file owner, Read to groups and Wrtie, Execute to Others: 
                             chmod u+rw, g+r, o+wx <file_name>
                                                     (OR)
                             chmod 643 <file_name>
Day 14: cut, awk, Crontab, date
CUT
The cut command in UNIX is a command for cutting out the sections column using a delimiter from each line of files and writing the result to standard output.
cut -d "delimiter" -f (field number) file.txt
    1) To cut the data with “ “ (space) as a delimiter and print the first column of data
        cut -d " " -f 1 state.txt
    2) To cut the data with “ “ (space) as delimiter and print first to fourth column data
        cut -d " " -f 1-4 state.txt
 
awk
 
The awk command in UNIX is a command for cutting out the sections column using a field separator from each line of files and writing the result to standard output.
 
    Consider the following text file as the input file for all cases below.
        $cat > employee.txt
          Ajay manager account 45000 
          Sunil clerk account 25000 
          varun manager sales 50000 
          Amit manager account 47000
 
1) Default behaviour of Awk: By default, Awk prints every line of data from the space-separated field of the file.
awk '{print $1}' employee.txt
                   (or)
awk -f " " '{print $1}' employee.txt
 
2) To print the last column of a file using NF – Number of Fields/Columns
     How to get the last word from a line in the file.
awk  ‘{print $NF}’ employee.txt
 
3) To match lines that contain a specific pattern using awk. To print lines containing "ERROR" in logfile.txt:
awk '/ERROR/ { print }' logfile.txt
4) print all columns except the first one column
awk '{$1=""; print $0}' file
5) print all columns except the last one column:
awk '{$NF=""; print $0}' file
Crontab (Job Scheduler)
The crontab is a list of commands that you want to run on a regular schedule, and also the name of the command used to manage that list. Crontab stands for “cron table, ” because it uses the job scheduler cron to execute tasks; cron itself is named after “chronos, ” the Greek word for time.cron is the system process which will automatically perform tasks for you according to a set schedule. The schedule is called the crontab, which is also the name of the program used to edit that schedule.
 
Linux Crontab Format:     *         *            *          *         *              <command to execute>
 
       MIN    HOUR     DOM     MON     DOW                  CMD
 
FIELD DESCRIPTION ALLOWED VALUE
•	MIN Minute field 0 to 59
•	HOUR Hour field 0 to 23
•	DOM Day of Month 1-31
•	MON Month field 1-12
•	DOW Day Of Week 0-6
•	CMD Command Any command to be executed.
 
To view the Crontab entries: crontab -l
To edit Crontab Entries: crontab -e
To edit crontab entries of other Linux users: crontab -u username -e
 
example
1) To schedule a job for every minute using Cron
* * * * * command/script


2) How to Execute a Linux Cron Jobs Every Second Using Crontab.
You cannot schedule an every-second cronjob. Because in cron the minimum unit you can specify is minute. 


3) To schedule a background Cron job for every 10 minutes.
*/10 * * * * /home/maverick/check-disk-space


4) Schedule a Job for More Than One Instance (e.g. Twice a Day)
executes the specified script at 11:00 and 16:00 every day
00 11,16 * * * /home/ramesh/bin/incremental-backup


5) Schedule a Job for Specific Range of Time (e.g. Only on Weekdays)
    This example checks the status of the database every day (including weekends) during the working hours 9 a.m – 6 p.m
00 09-18 * * * /home/ramesh/bin/check-db-status


6) Cron job to run on the last day of the month
55 23 28-31 * * [[ "$(date --date=tomorrow +\%d)" == "01" ]] && myscript.sh 0 23 28-31 * * [ $(date -d +1day +%d) -eq 1 ] && myscript.sh
 
7) Cron special keywords and their meaning Keyword Equivalent
@yearly 0 0 1 1 *
@daily 0 0 * * *
@hourly 0 * * * *
@reboot Run at startup.
 
a) To schedule a job for the first minute of every year using @yearly
@yearly /home/maverick/bin/annual-maintenance


b) To schedule a Cron job beginning of every month using @monthly
@monthly /home/maverick/bin/tape-backup


c) To schedule a background job every day using @daily
@daily /home/maverick/bin/cleanup-logs "day started"


d) To execute a Linux command after every reboot using @reboot
@reboot CMD
 
date
- date command is used to display the system date and time.
- date command is also used to set date and time of the system. 
- By default the date command displays the date in the time zone on which unix/linux operating system is configured. 
- You must be the super-user (root) to change the date and time.
a) Date and time of 2 years ago.    date --date="2 year ago"    Wed May 26 12:01:31 UTC 2021
b) Date and time of 5 seconds ago.    date --date="5 sec ago"        Fri May 26 12:01:37 UTC 2023
c) Date and time of previous day.    date --date="yesterday"        Thu May 25 12:01:51 UTC 2023
d) Date and time of 2 months ago.    date --date="2 month ago"    Sun Mar 26 12:02:00 UTC 2023
e) Date and time of 10 days ago.    date --date="10 day ago"    Tue May 16 12:02:10 UTC 2023
a) Upcoming particular week day.    date --date="next tue"        Tue May 30 00:00:00 UTC 2023
b) Date and time after two days.    date --date="2 day"        Sun May 28 12:03:03 UTC 2023
c) Date and time of next day.        date --date="tomorrow"        Sat May 27 12:03:11 UTC 2023
d) After 1 year on the current day.    date --date="1 year"        Sun May 26 12:03:20 UTC 2024
Formating 
date "+%D"        05/26/23
date "+%D %T"        05/26/23 05:49:30
date "+%Y-%m-%d"    2023-05-26
date "+%Y/%m/%d"    2023/05/26
date "+%A %B %d %T %y"    Friday May 26 05:49:30 23
 
CUT
The cut command in UNIX is a command for cutting out the sections column using a delimiter from each line of files and writing the result to standard output.
cut -d "delimiter" -f (field number) file.txt
    1) To cut the data with “ “ (space) as a delimiter and print the first column of data
        cut -d " " -f 1 state.txt
    2) To cut the data with “ “ (space) as delimiter and print first to fourth column data
        cut -d " " -f 1-4 state.txt
 
awk
 
The awk command in UNIX is a command for cutting out the sections column using a field separator from each line of files and writing the result to standard output.
 
    Consider the following text file as the input file for all cases below.
        $cat > employee.txt
          Ajay manager account 45000 
          Sunil clerk account 25000 
          varun manager sales 50000 
          Amit manager account 47000
 
1) Default behaviour of Awk: By default, Awk prints every line of data from the space-separated field of the file.
awk '{print $1}' employee.txt
                   (or)
awk -f " " '{print $1}' employee.txt
 
2) To print the last column of a file using NF – Number of Fields/Columns
     How to get the last word from a line in the file.
awk  ‘{print $NF}’ employee.txt
 
3) To match lines that contain a specific pattern using awk. To print lines containing "ERROR" in logfile.txt:
awk '/ERROR/ { print }' logfile.txt
4) print all columns except the first one column
awk '{$1=""; print $0}' file
5) print all columns except the last one column:
awk '{$NF=""; print $0}' file

Day 15: Background Process (&, bg, fg), Kill, /dev/null
RUN a process in Background in Linux
 
The & at the end of a command in Linux is used to run that command in the background immediately
 
<command> &
example: sleep 1000 &
See the list of backgorund jobs

 jobs 
   
Output: 
            [1]+  Stopped   sleep 1000
Bring process from background (bg) to foreground (fg) and vice versa
 
In Linux, fg and bg are commands used to manage jobs in the terminal — especially when you’ve paused or backgrounded a running process.
 
When you run a command in the terminal, it’s a job. You can have:
•	Foreground job: Takes over the terminal until done.
•	Background job: Runs behind the scenes while your terminal is still usable.
1.	Suspend (pause) the current foreground job: Ctrl + Z
2.	Resume to Running a suspended job in background: bg
3.	Bring a job back from brackground to foreground: fg
4.	List current jobs and their statuses: jobs
1.	Run a command that takes time:
sleep 1000
2.	Pause the job (send to background paused):
3.	Ctrl + Z
4.	
5.	#Check the list of background jobs
6.	jobs 
   Output: [1]+  Stopped   sleep 1000
7.	Resume it in the background only:
8.	 bg %1
9.	
10.	#Check the background jobs
11.	jobs 
   Output: [1]+  Running   sleep 1000
12.	Bring it back to foreground:
fg %1
/dev/null
•	/dev/null is a special device file in Linux often called the black hole.
•	Anything written to it → discarded
1.	Discard normal output (stdout)

2.	command > /dev/null
3.	              OR
command 1> /dev/null
4.	Discard error messages only (stderr)

command 2> /dev/null
5.	Discard everything (stdout + stderr)

6.	command &> /dev/null                           (BASH Only)
7.	                OR
command > /dev/null 2>&1
 
kill 
•	The kill command in Linux is used to terminate processes by sending them signals (default is SIGTERM, i.e., graceful termination).
•	It’s super handy when managing background or misbehaving processes.
kill [signal] PID
 
1. Graceful termination (default sends SIGTERM (signal 15))
kill <PID>
2. Force kill a process (sends SIGKILL (signal 9))
kill -9 <PID>
3. Kill background jobs using kill
kill %1
kill -9 %1
4. List available signal names
kill -l

Day 16: Shells
Linux Architecture 
 
 
Major Types of Linux Shells
Linux supports multiple shells like sh, bash, zsh, ksh, and fish, each providing different features for command execution and scripting.
1.	Bourne Shell (sh)
Original Unix shell - Lightweight, basic features
/bin/sh

2.	Bourne Again Shell (bash) Most Common
Enhanced version of sh - Default shell in Ubuntu and most linux 
/bin/bash


3.	C Shell (csh)
C-language-like syntax - Not recommended for scripting
/bin/csh


4.	Korn Shell (ksh)
Powerful scripting - Used in enterprise systems
/bin/ksh


5.	Z Shell (zsh) 
Advanced auto-completion - Used in macOS default shell
/bin/zsh
List All Available Shells
cat /etc/shells
Check Current Shell
echo $SHELL
Change Shell Temporarily
zsh
Change Shell Permanently
chsh -s /bin/zsh
Shell Startup Configuration Files
•	bash             ~/.bashrc, ~/.bash_profile
•	zsh               ~/.zshrc
•	csh               ~/.cshrc
•	ksh               ~/.kshrc
•	fish               ~/.config/fish/config.fish

Day 17: Doubt session
There is no notes available so watch video to know about xargs
