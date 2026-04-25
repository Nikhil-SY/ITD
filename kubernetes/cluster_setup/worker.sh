# #!/bin/bash

# set -e

# echo "=== Joining Kubernetes Cluster ==="

# bash /root/join.sh

# echo "=== WORKER JOINED SUCCESSFULLY ==="

#!/bin/bash

set -e

echo "=== STEP: Join Kubernetes Cluster ==="

if [ ! -f /root/join.sh ]; then
  echo "❌ join.sh not found. Copy it from master first."
  exit 1
fi

bash /root/join.sh

echo "=== WORKER NODE JOINED SUCCESSFULLY ==="