# Nginx: Forward Proxy, Reverse Proxy, Traffic Routing & Free SSL — Complete Guide

> **Who is this for?**  
> Anyone who wants to understand what proxies are, why they exist, how Nginx acts as a reverse proxy, and how to set up a production-ready web server that routes traffic to backend containers with HTTPS — explained from first principles with real examples.

---

## Table of Contents

1. [What is a Proxy? (The Analogy)](#1-what-is-a-proxy-the-analogy)
2. [Forward Proxy — What, Why, How](#2-forward-proxy--what-why-how)
3. [Reverse Proxy — What, Why, How](#3-reverse-proxy--what-why-how)
4. [Forward vs Reverse Proxy — Side-by-Side](#4-forward-vs-reverse-proxy--side-by-side)
5. [What is Nginx?](#5-what-is-nginx)
6. [How Nginx Acts as a Reverse Proxy](#6-how-nginx-acts-as-a-reverse-proxy)
7. [Nginx Directory Structure & Configuration Files](#7-nginx-directory-structure--configuration-files)
8. [Nginx Configuration Deep Dive](#8-nginx-configuration-deep-dive)
9. [Routing Traffic from Client to Backend Containers](#9-routing-traffic-from-client-to-backend-containers)
10. [Free SSL with Certbot](#10-free-ssl-with-certbot)
11. [Final sites-enabled Configuration (HTTP + HTTPS)](#11-final-sites-enabled-configuration-http--https)
12. [Testing & Troubleshooting](#12-testing--troubleshooting)
13. [Full Architecture Diagram](#13-full-architecture-diagram)

---

## 1. What is a Proxy? (The Analogy)

Imagine you want to send a letter to a company, but you don't want them to know your real home address. So you give the letter to a **middleman**, who sends it on your behalf. When the reply comes, the middleman receives it and forwards it to you.

That middleman is a **proxy**.

In networking, a proxy is a **server that sits between two parties** (usually a client and a server) and **relays requests and responses** between them. The proxy can:

- Hide the identity of one side
- Filter, cache, or log traffic
- Load-balance across multiple servers
- Add security layers (like SSL/TLS)

---

## 2. Forward Proxy — What, Why, How

### What is a Forward Proxy?

A **forward proxy** sits between a **client (user)** and the **internet**. The client sends its request TO the proxy, and the proxy forwards it to the destination server on the client's behalf.

```
Client ──────► Forward Proxy ──────► Internet (Google, YouTube, etc.)
         (request)            (forwards request)

Client ◄────── Forward Proxy ◄────── Internet
         (response)           (relays response)
```

> **Key point:** The destination server (Google, etc.) **sees the proxy's IP**, not the client's IP.

### Why Use a Forward Proxy?

| Use Case | Explanation |
|---|---|
| **Privacy / Anonymity** | Your real IP is hidden from websites |
| **Bypass geo-restrictions** | Access content blocked in your region (VPNs work similarly) |
| **Corporate internet control** | Companies route employee traffic through a proxy to block social media or adult sites |
| **Caching** | A school/office proxy can cache commonly visited pages, saving bandwidth |
| **Monitoring & Logging** | Track what websites employees or students visit |

### How it Works — Step by Step

1. You configure your browser or OS to use a proxy server (e.g., `192.168.1.10:3128`).
2. When you type `google.com`, your browser sends the request to the **proxy**, not directly to Google.
3. The proxy receives the request, checks its rules (is this site allowed?), then forwards it to Google.
4. Google responds to the **proxy's IP** (not yours).
5. The proxy relays the response back to your browser.

### Real-World Example

**Squid** is a popular open-source forward proxy. A company might configure:

```nginx
# /etc/squid/squid.conf (Squid forward proxy example)
http_port 3128
acl allowed_sites dstdomain .google.com .github.com
http_access allow allowed_sites
http_access deny all
```

This blocks all internet traffic **except** Google and GitHub — common in corporate environments.

### Forward Proxy — Visual

```
┌───────────────────────────────────────────────────────┐
│                  Corporate Network                    │
│                                                       │
│  [Employee Laptop] ──► [Forward Proxy :3128]          │
│                               │                       │
└───────────────────────────────┼───────────────────────┘
                                │
                         ┌──────▼──────┐
                         │  Internet   │
                         │  (Google,   │
                         │  YouTube)   │
                         └─────────────┘

Google only sees the Proxy's IP, not the Employee's IP.
```

---

## 3. Reverse Proxy — What, Why, How

### What is a Reverse Proxy?

A **reverse proxy** sits in front of **one or more backend servers** and handles requests **on their behalf**. This time, the **client doesn't know which backend server is handling the request** — they only talk to the reverse proxy.

```
Client ──────► Reverse Proxy ──────► Backend Server A
                                ├──► Backend Server B
                                └──► Backend Server C
```

> **Key point:** The client **sees only the reverse proxy's IP/domain**, not the actual backend servers.

### Why Use a Reverse Proxy?

| Use Case | Explanation |
|---|---|
| **Load Balancing** | Distribute traffic across multiple servers so no single one gets overloaded |
| **SSL Termination** | Handle HTTPS at the proxy level — backends only need to speak plain HTTP internally |
| **Security / Hiding backends** | Backend servers are not directly exposed to the internet |
| **Caching** | Cache responses from backends to reduce load |
| **Compression** | Compress responses (gzip) before sending to clients |
| **Single Entry Point** | Run multiple apps on different ports, all accessible via one domain |
| **A/B Testing** | Route some users to a new version of the app |

### How it Works — Step by Step

1. You type `https://myapp.com` in your browser.
2. DNS resolves `myapp.com` to the reverse proxy's IP address.
3. The reverse proxy receives your request on port 443 (HTTPS).
4. It reads the URL/path (e.g., `/api` or `/dashboard`) and decides which backend to forward to.
5. It forwards the request to the appropriate backend (e.g., `localhost:3000`).
6. The backend responds to the proxy.
7. The proxy relays the response back to your browser.

### Real-World Example

You run three apps:
- A **React frontend** on port `3000`
- A **Node.js API** on port `4000`
- A **Python FastAPI service** on port `5000`

You want all of them accessible via a single domain `myapp.com`:

```
https://myapp.com/          → React frontend  (port 3000)
https://myapp.com/api/      → Node.js API     (port 4000)
https://myapp.com/data/     → FastAPI service (port 5000)
```

Nginx (as reverse proxy) handles this routing automatically.

### Reverse Proxy — Visual

```
                         ┌─────────────────────────────┐
                         │        Your Server          │
                         │                             │
 [Browser]               │  ┌──────────────────────┐   │
     │                   │  │   Nginx Reverse Proxy  │   │
     │  HTTPS :443        │  │      Port 80/443      │   │
     └──────────────────►│  └──────────┬───────────┘   │
                         │             │                │
                         │    ┌────────┼────────┐       │
                         │    ▼        ▼        ▼       │
                         │  [React] [Node] [FastAPI]    │
                         │  :3000   :4000   :5000       │
                         └─────────────────────────────┘
```

---

## 4. Forward vs Reverse Proxy — Side-by-Side

| Feature | Forward Proxy | Reverse Proxy |
|---|---|---|
| **Sits in front of** | Clients | Servers |
| **Hides identity of** | Client (from internet) | Servers (from clients) |
| **Configured by** | Client / IT admin | Server admin / DevOps |
| **Primary purpose** | Outbound traffic control | Inbound traffic management |
| **Common tools** | Squid, HAProxy, VPN | Nginx, HAProxy, Traefik, Caddy |
| **Who uses it** | Corporate networks, VPNs | Every modern web application |
| **Client awareness** | Client is aware of the proxy | Client is NOT aware of backend servers |

---

## 5. What is Nginx?

**Nginx** (pronounced "engine-x") is a high-performance, open-source web server and reverse proxy server. Originally built to handle the "C10K problem" (serving 10,000 concurrent connections), it is now one of the most widely used web servers in the world.

Nginx can act as:
- A **web server** (serve static files like HTML, CSS, images)
- A **reverse proxy** (forward requests to backend apps)
- A **load balancer** (distribute traffic across multiple backends)
- An **HTTP cache**
- An **SSL/TLS terminator**

> **Think of Nginx as the receptionist of a large office building.** Every visitor (HTTP request) comes to the front desk (Nginx). The receptionist decides which department (backend service) the visitor should be sent to. Visitors never walk the hallways themselves — they're always guided.

---

## 6. How Nginx Acts as a Reverse Proxy

When Nginx receives an HTTP request, it evaluates:
1. **Which `server` block matches** the request's hostname (`Host` header)?
2. **Which `location` block matches** the request's URL path?
3. It then **`proxy_pass`es** the request to the configured upstream (backend).

The magic directive is:

```nginx
proxy_pass http://localhost:3000;
```

This one line tells Nginx: *"Take this request and forward it to whatever is running on port 3000 on this machine."*

---

## 7. Nginx Directory Structure & Configuration Files

After installing Nginx on Ubuntu/Debian, here is what the directory structure looks like:

```
/etc/nginx/
├── nginx.conf                  ← Main configuration file (global settings)
├── sites-available/            ← All virtual host config files live here
│   ├── default                 ← Default site (can be deleted)
│   └── myapp.com               ← Your custom site config
├── sites-enabled/              ← Symlinks to files in sites-available/
│   └── myapp.com → ../sites-available/myapp.com
├── conf.d/                     ← Additional config snippets (auto-loaded)
├── snippets/                   ← Reusable config pieces (e.g., SSL params)
│   └── fastcgi-php.conf
├── mime.types                  ← Maps file extensions to MIME types
└── modules-enabled/            ← Dynamically loaded modules
```

### Key Files Explained

#### `/etc/nginx/nginx.conf` — The Master Config

```nginx
# /etc/nginx/nginx.conf

user www-data;                    # OS user Nginx runs as
worker_processes auto;            # Number of worker processes (auto = one per CPU core)
pid /run/nginx.pid;               # File to store the master process ID

events {
    worker_connections 1024;      # Max connections per worker
}

http {
    ##
    # Basic Settings
    ##
    sendfile on;                  # Efficient file transfer (kernel-level)
    tcp_nopush on;                # Reduce network packets
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;          # Load MIME types
    default_type application/octet-stream;  # Fallback MIME type

    ##
    # Logging Settings
    ##
    access_log /var/log/nginx/access.log;   # Every request is logged here
    error_log /var/log/nginx/error.log;     # Errors logged here

    ##
    # Gzip Compression
    ##
    gzip on;                     # Enable compression for responses

    ##
    # Virtual Host Configs
    ##
    include /etc/nginx/conf.d/*.conf;           # Load from conf.d/
    include /etc/nginx/sites-enabled/*;         # Load active virtual hosts
}
```

#### `sites-available/` vs `sites-enabled/`

This is a Debian/Ubuntu convention:

- **`sites-available/`**: Store ALL your virtual host files here (active or not).
- **`sites-enabled/`**: Only **symlinks** to configs you want Nginx to actually use.

To enable a site:
```bash
sudo ln -s /etc/nginx/sites-available/myapp.com /etc/nginx/sites-enabled/myapp.com
```

To disable a site:
```bash
sudo rm /etc/nginx/sites-enabled/myapp.com
```

This pattern lets you toggle sites without deleting config files.

---

## 8. Nginx Configuration Deep Dive

### Core Building Blocks

Nginx configs are built from **blocks** (called **contexts**) and **directives**.

```
Contexts:          What they configure
──────────────────────────────────────
main               Global settings (worker processes, user)
  └── events       Connection handling
  └── http         All HTTP/HTTPS settings
        └── server One virtual host (one domain)
              └── location  URL path-specific settings
```

### The `server` Block

A `server` block defines a **virtual host** — a configuration for one domain or IP:

```nginx
server {
    listen 80;                      # Listen on port 80 (HTTP)
    server_name myapp.com www.myapp.com;  # Which domain(s) this block handles

    # ... location blocks go here
}
```

### The `location` Block

A `location` block matches **URL paths** and defines what to do with them:

```nginx
location / {
    # Match ALL requests (catch-all)
}

location /api/ {
    # Match requests starting with /api/
}

location = /favicon.ico {
    # EXACT match for /favicon.ico only
}

location ~* \.(jpg|png|gif)$ {
    # Regex match: any image file (case-insensitive)
}
```

### Location Match Priority (Most Specific Wins)

```
Priority (highest to lowest):
1. = /exact/path          Exact match
2. ^~ /prefix             Prefix match (stops regex search)
3. ~ regex                Case-sensitive regex
4. ~* regex               Case-insensitive regex
5. /prefix                Normal prefix match (lowest priority)
```

### The `proxy_pass` Directive

This is the heart of reverse proxying:

```nginx
location /api/ {
    proxy_pass http://localhost:4000;
    # Request: GET /api/users  →  forwarded as  GET /api/users  to :4000
}

location /api/ {
    proxy_pass http://localhost:4000/;   # Trailing slash matters!
    # Request: GET /api/users  →  forwarded as  GET /users  to :4000
    #          (the /api/ prefix is stripped)
}
```

> **Important:** A trailing slash on `proxy_pass` **strips** the `location` prefix from the forwarded URL. Without trailing slash, the full path is preserved.

### Essential Proxy Headers

When Nginx proxies a request, the backend receives a request from `127.0.0.1` (Nginx), not the original client. You need to pass these headers so your backend knows the real client info:

```nginx
location / {
    proxy_pass http://localhost:3000;

    # Pass the original client's IP address
    proxy_set_header X-Real-IP $remote_addr;

    # Pass the original client IP (chain-friendly, comma-separated)
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    # Tell the backend the original protocol (http or https)
    proxy_set_header X-Forwarded-Proto $scheme;

    # Pass the original Host header (the domain the client requested)
    proxy_set_header Host $host;

    # Required for websockets (upgrade connections)
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Timeout Directives

```nginx
location / {
    proxy_pass http://localhost:3000;

    proxy_connect_timeout 60s;   # Max time to establish connection to backend
    proxy_send_timeout    60s;   # Max time to send request to backend
    proxy_read_timeout    60s;   # Max time to wait for backend response
}
```

### Upstream Block (Load Balancing)

If you have multiple instances of the same service:

```nginx
upstream node_backend {
    server localhost:3000;        # Instance 1
    server localhost:3001;        # Instance 2
    server localhost:3002;        # Instance 3
    # Default: round-robin (requests cycle through instances)
}

server {
    listen 80;
    server_name myapp.com;

    location / {
        proxy_pass http://node_backend;  # Nginx will load-balance
    }
}
```

Load balancing strategies:
```nginx
upstream node_backend {
    least_conn;             # Send to server with fewest active connections
    # OR
    ip_hash;                # Same client IP always goes to same server (sticky sessions)

    server localhost:3000 weight=3;   # Gets 3x more traffic
    server localhost:3001 weight=1;   # Gets 1x traffic
}
```

---

## 9. Routing Traffic from Client to Backend Containers

### The Scenario

You have a Linux server with multiple Docker containers running different services:

| Service | Container Port | Description |
|---|---|---|
| React Frontend | `3000` | Your web UI |
| Node.js API | `4000` | REST API backend |
| Python FastAPI | `5000` | Data service |
| Grafana | `9090` | Monitoring dashboard |

You want:
- `https://myapp.com/` → React app
- `https://myapp.com/api/` → Node.js API
- `https://myapp.com/data/` → FastAPI service
- `https://monitoring.myapp.com/` → Grafana

### Step 1 — Install Nginx

```bash
sudo apt update
sudo apt install nginx -y

# Start Nginx and enable it on boot
sudo systemctl start nginx
sudo systemctl enable nginx

# Verify it's running
sudo systemctl status nginx

# Test config syntax (always do this before reloading)
sudo nginx -t
```

### Step 2 — Configure Your Docker Containers

Make sure your containers publish their ports to the host (but NOT to the public internet — Nginx will be the only public-facing service):

```yaml
# docker-compose.yml
version: '3'
services:
  frontend:
    image: my-react-app
    ports:
      - "127.0.0.1:3000:3000"   # Only accessible on localhost, not 0.0.0.0
  
  api:
    image: my-node-api
    ports:
      - "127.0.0.1:4000:4000"

  data-service:
    image: my-fastapi
    ports:
      - "127.0.0.1:5000:5000"

  grafana:
    image: grafana/grafana
    ports:
      - "127.0.0.1:9090:3000"
```

> **Security tip:** Binding to `127.0.0.1` means only processes on the same machine can connect — not the internet. Nginx, running on the same machine, CAN connect to `127.0.0.1:3000`.

### Step 3 — Create the Nginx Site Config (HTTP first)

```bash
sudo nano /etc/nginx/sites-available/myapp.com
```

```nginx
# /etc/nginx/sites-available/myapp.com

# Upstream definitions (optional but clean for load-balancing)
upstream frontend {
    server 127.0.0.1:3000;
}

upstream api {
    server 127.0.0.1:4000;
}

upstream data_service {
    server 127.0.0.1:5000;
}

# ──────────────────────────────────────────────
# Main site: myapp.com
# ──────────────────────────────────────────────
server {
    listen 80;
    listen [::]:80;                     # Also listen on IPv6
    server_name myapp.com www.myapp.com;

    # Logging (site-specific log files)
    access_log /var/log/nginx/myapp.access.log;
    error_log  /var/log/nginx/myapp.error.log;

    # ── React Frontend (catch-all: everything goes to React) ──
    location / {
        proxy_pass http://frontend;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # For React Router (client-side routing) — try files first, fallback to index.html
        proxy_intercept_errors on;
        error_page 404 = /index.html;
    }

    # ── Node.js API ──
    location /api/ {
        proxy_pass http://api/;           # Trailing slash strips /api/ prefix
                                          # So /api/users becomes /users at backend

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout    60s;
        proxy_read_timeout    60s;
    }

    # ── Python FastAPI Service ──
    location /data/ {
        proxy_pass http://data_service/;  # Strips /data/ prefix

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ── Static file optimization (if frontend serves its own static files) ──
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        proxy_pass http://frontend;
        proxy_cache_valid 200 1d;         # Cache static files for 1 day
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}

# ──────────────────────────────────────────────
# Subdomain: monitoring.myapp.com
# ──────────────────────────────────────────────
server {
    listen 80;
    listen [::]:80;
    server_name monitoring.myapp.com;

    location / {
        proxy_pass http://127.0.0.1:9090;

        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 4 — Enable the Site and Test

```bash
# Create symlink to enable the site
sudo ln -s /etc/nginx/sites-available/myapp.com /etc/nginx/sites-enabled/myapp.com

# Remove the default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test configuration for syntax errors
sudo nginx -t

# Expected output:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# Reload Nginx (no downtime)
sudo systemctl reload nginx
```

---

## 10. Free SSL with Certbot

### What is SSL/TLS and Why Do You Need It?

**SSL (Secure Sockets Layer)** / **TLS (Transport Layer Security)** encrypts the communication between a client's browser and your server.

Without SSL:
```
Browser ──── HTTP ──►  [Your Server]
        Plain text, anyone can read it (passwords, data, etc.)
```

With SSL:
```
Browser ──── HTTPS ──►  [Your Server]
        Encrypted: even if intercepted, unreadable
```

Browsers show a **🔒 padlock** for HTTPS sites and warn users about HTTP sites. Google also ranks HTTPS sites higher in search results.

### What is Let's Encrypt?

**Let's Encrypt** is a free, automated Certificate Authority (CA). It issues SSL certificates that browsers trust — for free. You don't need to pay $100/year for SSL anymore.

### What is Certbot?

**Certbot** is the official client tool for Let's Encrypt. It:
1. Proves you own the domain (by serving a challenge file or modifying DNS)
2. Downloads the certificate
3. **Automatically modifies your Nginx config** to use HTTPS
4. Sets up **automatic renewal** (certificates expire every 90 days)

### Step 1 — Open Firewall Ports

```bash
# Allow HTTP and HTTPS through the firewall
sudo ufw allow 'Nginx Full'   # Opens both port 80 and 443
sudo ufw status
```

### Step 2 — Install Certbot

```bash
# Install Certbot and the Nginx plugin
sudo apt install certbot python3-certbot-nginx -y
```

### Step 3 — Obtain SSL Certificate

Make sure your domain's DNS A record points to your server's public IP before running this.

```bash
# Get certificates for both the apex domain and www subdomain
sudo certbot --nginx -d myapp.com -d www.myapp.com

# For the monitoring subdomain
sudo certbot --nginx -d monitoring.myapp.com
```

Certbot will ask:
1. Your email address (for expiry notifications)
2. Agree to Terms of Service → `A`
3. Whether to redirect HTTP to HTTPS → **Choose option 2 (Redirect)** — always recommended

### What Certbot Does Automatically

Certbot modifies your Nginx config to add:
- SSL certificate paths
- Redirect from HTTP (port 80) to HTTPS (port 443)

### Step 4 — Verify Auto-Renewal

Certbot installs a **cron job** or **systemd timer** that renews certificates before they expire:

```bash
# Test that automatic renewal works
sudo certbot renew --dry-run

# Check the systemd timer
sudo systemctl status certbot.timer

# Manually list certificates and expiry dates
sudo certbot certificates
```

---

## 11. Final sites-enabled Configuration (HTTP + HTTPS)

After running Certbot, your config will look like this (or you can write it manually for full control):

```bash
sudo nano /etc/nginx/sites-available/myapp.com
```

```nginx
# /etc/nginx/sites-available/myapp.com
# Complete production configuration with HTTPS, HTTP→HTTPS redirect,
# reverse proxy to Docker containers, security headers, and gzip.

# ──────────────────────────────────────────────
# Upstream blocks
# ──────────────────────────────────────────────
upstream frontend {
    server 127.0.0.1:3000;
}

upstream api {
    server 127.0.0.1:4000;
}

upstream data_service {
    server 127.0.0.1:5000;
}

# ──────────────────────────────────────────────
# SERVER BLOCK 1: HTTP → HTTPS redirect
# Catches all HTTP traffic and permanently redirects to HTTPS
# ──────────────────────────────────────────────
server {
    listen 80;
    listen [::]:80;
    server_name myapp.com www.myapp.com;

    # Let's Encrypt certificate challenge (DO NOT REMOVE — needed for renewal)
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Redirect ALL other HTTP traffic to HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

# ──────────────────────────────────────────────
# SERVER BLOCK 2: HTTPS main site
# ──────────────────────────────────────────────
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;                           # Enable HTTP/2 for better performance
    server_name myapp.com www.myapp.com;

    # ── SSL Certificate Paths (filled in by Certbot) ──
    ssl_certificate     /etc/letsencrypt/live/myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.com/privkey.pem;

    # ── SSL Security Settings ──
    ssl_protocols TLSv1.2 TLSv1.3;           # Only allow modern, secure protocols
    ssl_prefer_server_ciphers off;            # Let clients choose cipher (TLS 1.3 best practice)
    ssl_session_cache shared:SSL:10m;         # Cache SSL sessions for performance
    ssl_session_timeout 1d;
    ssl_session_tickets off;                  # Disable for better forward secrecy

    # ── HSTS: Tell browsers to ALWAYS use HTTPS for 1 year ──
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # ── Security Headers ──
    add_header X-Frame-Options SAMEORIGIN always;              # Prevent clickjacking
    add_header X-Content-Type-Options nosniff always;          # Prevent MIME sniffing
    add_header X-XSS-Protection "1; mode=block" always;       # XSS protection
    add_header Referrer-Policy "no-referrer-when-downgrade" always;

    # ── Logging ──
    access_log /var/log/nginx/myapp.access.log;
    error_log  /var/log/nginx/myapp.error.log warn;

    # ── Gzip Compression ──
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;                      # Don't compress tiny files
    gzip_types
        text/plain
        text/css
        text/javascript
        application/javascript
        application/json
        application/xml
        image/svg+xml;

    # ── Client Upload Size ──
    client_max_body_size 50M;                  # Allow up to 50MB uploads

    # ────────────────────────────────────────
    # LOCATION BLOCKS — URL Routing
    # ────────────────────────────────────────

    # ── Static Asset Caching (served by React container) ──
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|map)$ {
        proxy_pass http://frontend;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        expires 30d;
        add_header Cache-Control "public, max-age=2592000, immutable";
    }

    # ── Node.js API (path: /api/) ──
    location /api/ {
        proxy_pass http://api/;            # Strips /api/ prefix before forwarding

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (if your API uses WebSockets)
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";

        proxy_connect_timeout 60s;
        proxy_send_timeout    60s;
        proxy_read_timeout    60s;

        # Disable buffering for SSE / streaming responses
        proxy_buffering off;
    }

    # ── Python FastAPI (path: /data/) ──
    location /data/ {
        proxy_pass http://data_service/;   # Strips /data/ prefix

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_read_timeout    120s;        # Longer timeout for data-heavy endpoints
    }

    # ── React Frontend (catch-all — must be LAST) ──
    location / {
        proxy_pass http://frontend;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (for React hot-reload in dev)
        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";

        # Handle React Router — if backend returns 404, try index.html
        proxy_intercept_errors on;
        error_page 404 = @fallback;
    }

    # Fallback to React's index.html for client-side routing
    location @fallback {
        proxy_pass http://frontend/index.html;
        proxy_set_header Host $host;
    }
}

# ──────────────────────────────────────────────
# SERVER BLOCK 3: monitoring.myapp.com (subdomain)
# ──────────────────────────────────────────────
server {
    listen 80;
    listen [::]:80;
    server_name monitoring.myapp.com;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    http2 on;
    server_name monitoring.myapp.com;

    ssl_certificate     /etc/letsencrypt/live/monitoring.myapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/monitoring.myapp.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    add_header Strict-Transport-Security "max-age=31536000" always;

    # Optional: restrict Grafana access by IP
    # allow 103.x.x.x;      # Your office IP
    # deny all;

    location / {
        proxy_pass http://127.0.0.1:9090;

        proxy_http_version 1.1;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Enable and Reload

```bash
# Test configuration
sudo nginx -t

# Reload Nginx (graceful — no dropped connections)
sudo systemctl reload nginx

# If something is wrong, check the error log
sudo tail -f /var/log/nginx/myapp.error.log
```

---

## 12. Testing & Troubleshooting

### Test Your Configuration

```bash
# Test Nginx config syntax
sudo nginx -t

# Check which config files are loaded
sudo nginx -T | head -50

# Check Nginx status
sudo systemctl status nginx

# View real-time access logs
sudo tail -f /var/log/nginx/myapp.access.log

# View real-time error logs
sudo tail -f /var/log/nginx/myapp.error.log
```

### Test SSL Certificate

```bash
# Test that HTTPS works
curl -I https://myapp.com

# Check certificate expiry date
echo | openssl s_client -connect myapp.com:443 2>/dev/null | openssl x509 -noout -dates

# Test HTTP → HTTPS redirect
curl -I http://myapp.com
# Should see: HTTP/1.1 301 Moved Permanently
# Location: https://myapp.com/
```

### Test Backend Connectivity

```bash
# Make sure backend containers are reachable from the host
curl http://127.0.0.1:3000     # Frontend
curl http://127.0.0.1:4000     # API
curl http://127.0.0.1:5000     # Data service

# Check which ports are listening
ss -tlnp | grep nginx
ss -tlnp | grep docker
```

### Common Errors and Fixes

| Error | Likely Cause | Fix |
|---|---|---|
| `502 Bad Gateway` | Backend container is down or not on expected port | Check `docker ps`, verify ports |
| `504 Gateway Timeout` | Backend is too slow or hanging | Increase `proxy_read_timeout` |
| `403 Forbidden` | Nginx can't read files OR IP blocked | Check file permissions or `allow/deny` directives |
| `404 Not Found` | No location block matched | Check your `location` blocks |
| `nginx: [emerg] bind() to 0.0.0.0:443 failed` | Port 443 already in use | Check `sudo ss -tlnp | grep 443` |
| Certificate not trusted | Using self-signed cert | Use Certbot / Let's Encrypt |
| `413 Request Entity Too Large` | File upload too big | Increase `client_max_body_size` |

### Nginx Reload vs Restart

```bash
sudo systemctl reload nginx    # Graceful: finishes existing requests, then applies new config
sudo systemctl restart nginx   # Kills all connections immediately (use only if reload fails)
```

---

## 13. Full Architecture Diagram

```
                              INTERNET
                                 │
                    HTTPS (443) / HTTP (80)
                                 │
                    ┌────────────▼────────────┐
                    │         SERVER          │
                    │                         │
                    │  ┌───────────────────┐  │
                    │  │   UFW Firewall    │  │
                    │  │  (Allow 80, 443)  │  │
                    │  └─────────┬─────────┘  │
                    │            │             │
                    │  ┌─────────▼─────────┐  │
                    │  │      NGINX        │  │
                    │  │  Reverse Proxy    │  │
                    │  │                   │  │
                    │  │ • SSL Termination │  │
                    │  │ • HTTP→HTTPS      │  │
                    │  │ • Path Routing    │  │
                    │  │ • Load Balancing  │  │
                    │  │ • Security Headers│  │
                    │  └──┬──────┬──────┬──┘  │
                    │     │      │      │      │
                    │     ▼      ▼      ▼      │
                    │  ┌──────┐ ┌───┐ ┌────┐  │
                    │  │React │ │API│ │Fast│  │
                    │  │:3000 │ │:4000│ │API │  │
                    │  │      │ │   │ │:5000│  │
                    │  └──────┘ └───┘ └────┘  │
                    │     Docker Containers    │
                    └─────────────────────────┘

URL Routing:
──────────────────────────────────────────────
https://myapp.com/          →  localhost:3000 (React)
https://myapp.com/api/*     →  localhost:4000 (Node.js)
https://myapp.com/data/*    →  localhost:5000 (FastAPI)
https://monitoring.myapp.com →  localhost:9090 (Grafana)
──────────────────────────────────────────────

SSL Certificate: Let's Encrypt (Free, auto-renews every 90 days)
Certbot Timer:   Runs twice daily, renews if < 30 days to expiry
```

---

## Quick Reference Cheat Sheet

```bash
# Install
sudo apt install nginx certbot python3-certbot-nginx -y

# Site management
sudo ln -s /etc/nginx/sites-available/myapp.com /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/myapp.com

# Test & reload
sudo nginx -t && sudo systemctl reload nginx

# Get SSL certificate
sudo certbot --nginx -d myapp.com -d www.myapp.com

# Renew SSL
sudo certbot renew --dry-run

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Debug
sudo nginx -T           # Print full merged config
curl -I https://myapp.com   # Test HTTPS response headers
```

---

*Guide covers: Ubuntu 22.04/24.04 LTS · Nginx 1.18+ · Certbot 2.x · Docker Compose v2*