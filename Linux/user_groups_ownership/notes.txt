================================================================================
LINUX USER, GROUP, AND OWNERSHIP MANAGEMENT
================================================================================

1. USER MANAGEMENT
================================================================================

/**
 * ADDING USERS:
 * 
 * useradd vs adduser:
 * - useradd: Low-level utility for adding users. Requires manual configuration of shell, home directory, etc.
 *            More control but more manual setup needed. Available on all Linux systems.
 * - adduser: High-level wrapper around useradd (Debian/Ubuntu). Automatically creates home directory,
 *            sets up shell interactively. More user-friendly with sensible defaults.
 * 
 * usermod -aG vs usermod -g:
 * - usermod -g: Changes the primary group of a user. Replaces the existing primary group.
 *               Only one primary group can be set. Example: usermod -g groupname username
 * - usermod -aG: Adds user to a supplementary group without changing primary group.
 *                The -a flag means "append". User can belong to multiple supplementary groups.
 *                Example: usermod -aG groupname username
 * 
 * Note: Use -aG for adding to additional groups. Use -g only when intentionally changing primary group.
 */
ADDING USERS:
    useradd username
        Example: useradd john
        Arguments: -m (create home), -s (shell), -g (group), -G (groups)
        Example: useradd -m -s /bin/bash -g users john

    adduser username (interactive)
        Example: adduser john

DELETING USERS:
    userdel username
        Example: userdel john
        Arguments: -r (remove home directory)
        Example: userdel -r john

MODIFYING USERS:
    usermod [options] username
        Example: usermod -c "John Doe" john
        Arguments: -c (comment), -d (home dir), -s (shell), -G (groups)
        Example: usermod -G wheel,sudo john

CHANGING PASSWORD:
    passwd username
        Example: passwd john


2. GROUP MANAGEMENT
================================================================================

ADDING GROUPS:
    groupadd groupname
        Example: groupadd developers
        Arguments: -g (GID), -S (system group)
        Example: groupadd -g 1005 developers

DELETING GROUPS:
    groupdel groupname
        Example: groupdel developers

MODIFYING GROUPS:
    groupmod [options] groupname
        Example: groupmod -n newname oldname
        Arguments: -n (new name), -g (new GID)

ADDING USER TO GROUP:
    usermod -aG groupname username
        Example: usermod -aG developers john
        Arguments: -a (append), -G (groups)

REMOVING USER FROM GROUP:
    gpasswd -d username groupname
        Example: gpasswd -d john developers


3. OWNERSHIP MANAGEMENT
================================================================================

CHANGING OWNER:
    chown user filename
        Example: chown john file.txt
        Arguments: -R (recursive), -v (verbose)
        Example: chown -R john /home/john/documents

CHANGING GROUP:
    chgrp group filename
        Example: chgrp developers file.txt
        Arguments: -R (recursive), -v (verbose)
        Example: chgrp -R developers /home/john/projects

CHANGING OWNER AND GROUP:
    chown user:group filename
        Example: chown john:developers file.txt
        Example: chown -R john:developers /home/john/projects


4. VIEWING USER/GROUP/OWNERSHIP INFO
================================================================================

VIEW ALL USERS:
    cat /etc/passwd

VIEW ALL GROUPS:
    cat /etc/group

VIEW FILE OWNERSHIP:
    ls -l filename
        Example: ls -l file.txt
        Output: -rw-r--r-- 1 john developers 1234 Jan 1 12:00 file.txt

VIEW USER GROUPS:
    groups username
        Example: groups john


5. PRACTICAL EXAMPLES
================================================================================

SCENARIO 1: Create developer user with home directory
    useradd -m -s /bin/bash -g developers john
    passwd john

SCENARIO 2: Add user to multiple groups
    usermod -aG wheel,docker,developers john

SCENARIO 3: Change file ownership recursively
    chown -R john:developers /var/www/project

SCENARIO 4: Set up project directory
    mkdir /opt/project
    chown john:developers /opt/project
    chmod 770 /opt/project