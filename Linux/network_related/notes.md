================================================================================
FUNDAMENTAL NETWORK COMMANDS
================================================================================

1. PING
    Purpose: Test connectivity to a host
    Syntax: ping [hostname/IP]
    Example: ping google.com
    Use Case: Verify if a server is reachable
    Output: Shows response time and packet loss

2. IFCONFIG / IP ADDR
    Purpose: Display network interface configuration
    Syntax: ifconfig (older) or ip addr show (newer)
    Example: ip addr show
    Use Case: Check IP address, MAC address, interface status
    Shows: IP, netmask, broadcast address, MAC address

3. NETSTAT / SS
    Purpose: Display network statistics and connections
    Syntax: netstat -tuln or ss -tuln
    Example: ss -tuln | grep LISTEN
    Use Case: Monitor open ports and active connections
    Real case: Check if port 80 is being used

4. NSLOOKUP / DIG
    Purpose: DNS lookup to resolve domain names
    Syntax: nslookup google.com or dig google.com
    Example: dig example.com +short
    Use Case: Troubleshoot DNS issues
    Real case: Find IP of a website

5. TRACEROUTE
    Purpose: Trace the path packets take to destination
    Syntax: traceroute [hostname/IP]
    Example: traceroute google.com
    Use Case: Diagnose network latency issues
    Real case: Identify where connection fails

6. ROUTE
    Purpose: Display/modify routing table
    Syntax: route -n or ip route show
    Example: route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.0.1
    Use Case: Configure network routing
    Real case: Add static route for VPN

7. ARP
    Purpose: Display ARP (Address Resolution Protocol) table
    Syntax: arp -a or ip neigh show
    Example: arp -a
    Use Case: Map IP addresses to MAC addresses
    Real case: Find which device has conflicting IP

8. HOSTNAME
    Purpose: Display or set system hostname
    Syntax: hostname or hostnamectl set-hostname newname
    Example: hostnamectl set-hostname server-01
    Use Case: Identify system on network
    Real case: Rename a server for organization

9. CURL / WGET
    Purpose: Download files or make HTTP requests
    Syntax: curl [URL] or wget [URL]
    Example: curl -I https://example.com
    Use Case: Test API endpoints, download files
    Real case: Check website availability

10. NETCAT (NC)
     Purpose: Read/write data across networks
     Syntax: nc -l -p [port] or nc [host] [port]
     Example: nc -l -p 9999 (listen) or nc localhost 9999 (connect)
     Use Case: Port scanning, data transfer, debugging
     Real case: Test if port is open

11. WHOIS
     Purpose: Lookup domain registration information
     Syntax: whois [domain]
     Example: whois google.com
     Use Case: Get domain owner details
     Real case: Find contact info for domain

12. IPTABLES / UMEWALL
     Purpose: Configure firewall rules
     Syntax: iptables -A INPUT -p tcp --dport 80 -j ACCEPT
     Example: ufw allow 22/tcp
     Use Case: Control incoming/outgoing traffic
     Real case: Block IP address or specific port

13. TCPDUMP
     Purpose: Capture and analyze network packets
     Syntax: tcpdump -i [interface] -n
     Example: tcpdump -i eth0 -n 'tcp port 80'
     Use Case: Diagnose network issues, security analysis
     Real case: Monitor HTTP traffic for debugging

14. WGET / CURL WITH OPTIONS
     Purpose: Advanced HTTP operations
     Example: curl -X POST -d "data" https://api.example.com
     Use Case: Test APIs, automation
     Real case: Send data to remote server

================================================================================
PRACTICAL REAL-WORLD SCENARIOS
================================================================================

SCENARIO 1: Server is unreachable
- Step 1: ping server-ip
- Step 2: traceroute server-ip (find where it fails)
- Step 3: Check firewall: sudo iptables -L

SCENARIO 2: Port already in use
- Step 1: sudo ss -tuln | grep :8080
- Step 2: Find process: sudo lsof -i :8080
- Step 3: Kill if needed: sudo kill -9 [PID]

SCENARIO 3: Website not loading
- Step 1: ping website.com
- Step 2: dig website.com (check DNS)
- Step 3: curl -v https://website.com (check HTTP response)

SCENARIO 4: Slow network performance
- Step 1: ping -c 10 destination (check latency/loss)
- Step 2: traceroute destination (identify slow hop)
- Step 3: tcpdump -i eth0 -n (capture packets)

SCENARIO 5: Configure static IP
- Step 1: ip addr show (current config)
- Step 2: sudo nano /etc/network/interfaces
- Step 3: Add: auto eth0 / iface eth0 inet static / address 192.168.1.10
- Step 4: sudo systemctl restart networking

================================================================================

**real DevOps-grade Linux troubleshooting**

I’ll explain each command in this format:

1. **Why we use it**
2. **Command syntax**
3. **Every important option explained**
4. **Real troubleshooting scenarios**
5. **How to interpret output**
6. **When to choose this over similar commands**

---

# 1. `ping` — Layer 3 Connectivity Test

## Purpose

Tests **ICMP reachability**.

Answers:

* Can I reach host?
* Packet loss?
* Latency?
* DNS resolution issue?

---

## Syntax

```bash
ping [options] host
```

Example:

```bash
ping google.com
```

Output:

```text
64 bytes from 142.250.183.14: icmp_seq=1 ttl=117 time=32 ms
```

---

## Important options

### `-c`

Count packets.

```bash
ping -c 4 google.com
```

Send only 4 packets.

Useful in scripts.

---

### `-i`

Interval between packets.

```bash
ping -i 0.5 google.com
```

Send every 0.5 sec.

Default = 1 sec.

---

### `-s`

Packet size.

```bash
ping -s 1500 google.com
```

Useful for **MTU troubleshooting**.

Example:
VPN issue → large packets dropped.

---

### `-W`

Timeout per reply.

```bash
ping -W 2 google.com
```

Wait only 2 sec.

---

### `-I`

Specify source interface.

```bash
ping -I eth0 8.8.8.8
```

Useful on multi-NIC servers.

---

## Output explanation

```text
64 bytes from 8.8.8.8: icmp_seq=1 ttl=57 time=20 ms
```

### `icmp_seq`

Packet number.

Missing numbers → packet loss.

---

### `ttl`

Time To Live.

Helps infer hops/OS.

Example:

```text
ttl=64 → Linux
ttl=128 → Windows
```

---

### `time`

Latency.

High time = slow network.

---

## Troubleshooting examples

### DNS issue?

```bash
ping google.com
```

Fails.

Try:

```bash
ping 8.8.8.8
```

Works.

Means:

**Network OK, DNS broken**

---

### Network unreachable

```text
Destination Host Unreachable
```

Likely:

* routing issue
* gateway down

---

---

# 2. `nslookup`

## Purpose

Quick DNS query tool.

Checks:

* A record
* CNAME
* MX
* DNS server behavior

---

## Syntax

```bash
nslookup domain
```

Example:

```bash
nslookup google.com
```

Output:

```text
Server: 8.8.8.8
Address: 8.8.8.8#53

Name: google.com
Address: 142.250.x.x
```

---

## Query specific record

### MX

```bash
nslookup -type=MX gmail.com
```

Mail servers.

---

### CNAME

```bash
nslookup -type=CNAME www.example.com
```

---

### NS

```bash
nslookup -type=NS example.com
```

Name servers.

---

## Query specific DNS server

```bash
nslookup myapp.company.com 8.8.8.8
```

Useful when comparing internal DNS vs public DNS.

---

## Real troubleshooting

### Internal hostname not resolving

```bash
nslookup internal-api.company.local
```

NXDOMAIN.

Check company DNS:

```bash
nslookup internal-api.company.local 10.0.0.2
```

Works.

Problem = wrong resolver in `/etc/resolv.conf`

---

## Limitation

Old tool.

Prefer **dig** for detailed analysis.

---

# 3. `dig` (Best DNS tool)

## Why better than nslookup

Shows:

* TTL
* authority section
* query time
* recursion
* exact DNS answer

---

## Syntax

```bash
dig domain
```

---

## Important sections

Example:

```bash
dig google.com
```

Output:

```text
QUESTION SECTION
ANSWER SECTION
AUTHORITY SECTION
ADDITIONAL SECTION
```

---

## Important options

### `+short`

Cleaner output.

```bash
dig google.com +short
```

Output:

```text
142.250.183.14
```

Great for scripting.

---

### Query record type

```bash
dig google.com MX
```

---

### Query specific DNS server

```bash
dig @8.8.8.8 google.com
```

---

### Trace delegation

```bash
dig +trace google.com
```

Shows:

root → TLD → authoritative DNS

Useful when DNS propagation issues.

---

### Reverse lookup

```bash
dig -x 8.8.8.8
```

PTR record.

---

## Real troubleshooting

### DNS propagation issue

```bash
dig myapp.com
```

Old IP returned.

Check authoritative:

```bash
dig @ns1.provider.com myapp.com
```

Shows new IP.

Means:
Public cache not updated.

---

# 4. `traceroute`

## Purpose

Shows **network path** (hop by hop).

Useful for:

* packet loss location
* routing loops
* slow network segment

---

## Syntax

```bash
traceroute google.com
```

May need install:

```bash
sudo apt install traceroute
```

---

## Important options

### `-n`

No DNS resolution.

```bash
traceroute -n google.com
```

Much faster.

---

### `-I`

Use ICMP instead of UDP.

```bash
traceroute -I google.com
```

---

### `-T`

TCP SYN mode.

```bash
traceroute -T -p 443 google.com
```

Best when firewalls block ICMP.

---

### `-m`

Max hops.

```bash
traceroute -m 20 google.com
```

---

## Reading output

```text
1 10.0.0.1
2 172.16.0.1
3 *
4 *
5 8.8.8.8
```

`*` means:

* ICMP blocked
* timeout

Not always failure.

---

## Real troubleshooting

App in AWS unreachable.

Run:

```bash
traceroute api.company.com
```

Stops at corporate firewall.

Root cause:
Firewall issue.

---

# 5. `netstat`

Older but useful.

## Purpose

Check:

* listening ports
* connections
* routing table
* interfaces

---

## Common syntax

```bash
netstat -tulnp
```

### Breakdown

`-t` TCP
`-u` UDP
`-l` listening
`-n` numeric
`-p` process

---

Example:

```bash
netstat -tulnp | grep 8080
```

Output:

```text
tcp 0 0 0.0.0.0:8080 LISTEN 2345/java
```

Means Java listening.

---

## Other useful options

### `-an`

All sockets.

```bash
netstat -an
```

---

### `-rn`

Routing table.

```bash
netstat -rn
```

---

### `-i`

Interface stats.

```bash
netstat -i
```

---

## Limitation

Deprecated.

Prefer `ss`.

---

# 6. `ss` (Modern netstat)

Fast socket inspection.

---

## Syntax

```bash
ss -tulnp
```

Same meaning as netstat.

---

## Important options

### Established connections

```bash
ss -ant
```

---

### Listening only

```bash
ss -lnt
```

---

### Process info

```bash
ss -p
```

---

### Filter by port

```bash
ss -lnt '( sport = :443 )'
```

Very powerful filtering.

---

## Troubleshooting example

App says "port already in use"

Check:

```bash
ss -lntp | grep 8080
```

Find offending PID.

---

# 7. `lsof`

**List Open Files**

In Linux, sockets are files.

Amazing tool.

---

## Find process using port

```bash
lsof -i :8080
```

Output:

```text
java 2345 user TCP *:8080 (LISTEN)
```

---

## Important options

### `-i`

Network files.

```bash
lsof -i
```

---

### `-p`

Specific PID.

```bash
lsof -p 2345
```

See all files opened by process.

---

### `+D`

Directory usage.

```bash
lsof +D /var/log
```

Who is holding files.

---

## Real troubleshooting

Cannot delete log file.

Reason:
Process still holding file handle.

Check:

```bash
lsof | grep deleted
```

Classic Linux issue.

---

# 8. `netcat (nc)`

Swiss army knife.

---

## Test TCP port

```bash
nc -zv google.com 443
```

Options:

`-z` scan only
`-v` verbose

Output:

```text
succeeded
```

---

## Test UDP

```bash
nc -zvu dns.server 53
```

---

## Listen on port

```bash
nc -l 9000
```

---

## Send data manually

```bash
echo "hello" | nc host 9000
```

---

## Real troubleshooting

Check if remote DB reachable:

```bash
nc -zv db-server 5432
```

Success:
Network path OK.

Failure:
Firewall or service issue.

---

# 9. `telnet`

Old but useful for manual TCP tests.

---

## Test connection

```bash
telnet host 443
```

If connects:

```text
Connected to host
```

---

## Manual HTTP test

```bash
telnet mysite.com 80
GET /
```

See raw HTTP response.

---

Prefer `nc`, but telnet still handy.

---

# 10. `systemctl`

Manage systemd services.

---

## Check status

```bash
systemctl status nginx
```

Shows:

* active/inactive
* PID
* recent logs

---

## Important commands

### Start

```bash
systemctl start nginx
```

---

### Stop

```bash
systemctl stop nginx
```

---

### Restart

```bash
systemctl restart nginx
```

---

### Reload config

```bash
systemctl reload nginx
```

No downtime.

---

### Enable boot

```bash
systemctl enable nginx
```

---

### Dependencies

```bash
systemctl list-dependencies nginx
```

---

### Failed units

```bash
systemctl --failed
```

Very useful.

---

# 11. `journalctl`

Systemd logs.

Better than checking files manually.

---

## Service logs

```bash
journalctl -u nginx
```

---

## Follow logs

```bash
journalctl -u nginx -f
```

Like tail -f.

---

## Boot logs

```bash
journalctl -b
```

Previous boot:

```bash
journalctl -b -1
```

Great for reboot failures.

---

## Time filter

```bash
journalctl --since "1 hour ago"
```

---

## Priority filter

```bash
journalctl -p err
```

Only errors.

Levels:

* emerg
* alert
* crit
* err
* warning
* notice
* info
* debug

---

## Output without truncation

```bash
journalctl -xe
```

`-x` explanation
`-e` jump end

---

# Other powerful networking commands

---

# `ip`

Modern replacement for ifconfig.

## Interfaces

```bash
ip addr
```

---

## Routing

```bash
ip route
```

---

## Neighbor table

```bash
ip neigh
```

ARP troubleshooting.

---

# `curl`

Best app-level test.

```bash
curl -v https://myapp.com
```

Shows:

* DNS
* TCP connect
* TLS handshake
* headers

Amazing for debugging.

---

# `tcpdump`

Packet capture.

Most powerful troubleshooting tool.

Example:

```bash
sudo tcpdump -i eth0 port 443
```

See actual packets.

Use when nothing else explains issue.

---

# Practical DevOps Troubleshooting Flow

App unreachable:

### Step 1

```bash
ping host
```

Reachable?

---

### Step 2

```bash
dig host
```

DNS OK?

---

### Step 3

```bash
traceroute host
```

Path OK?

---

### Step 4

```bash
nc -zv host 443
```

Port reachable?

---

### Step 5

```bash
ss -tulnp
```

Is app listening?

---

### Step 6

```bash
systemctl status app
```

Running?

---

### Step 7

```bash
journalctl -u app -f
```

Logs.

---

### Step 8

```bash
tcpdump
```

Packet-level debugging.

---

This is the real troubleshooting stack most senior DevOps engineers use.
