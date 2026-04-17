#!/bin/bash

# showip - Simple network interface display wrapper
# Parses 'ip addr show' output and displays it cleanly

show_usage() {
    echo "Usage: showip [interface] [--help]"
    echo ""
    echo "Display network interface information"
    echo ""
    echo "Examples:"
    echo "  showip              # Show all interfaces"
    echo "  showip eth0         # Show specific interface"
    echo "  showip --help       # This message"
}

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_usage
    exit 0
fi

# If argument provided, filter by interface
if [[ -n "$1" ]]; then
    INTERFACE="$1"
    ip_output=$(ip addr show "$INTERFACE" 2>/dev/null)
    if [[ $? -ne 0 ]]; then
        echo "Error: Interface '$INTERFACE' not found"
        exit 1
    fi
else
    INTERFACE=""
    ip_output=$(ip addr show)
fi

echo "=== Network Interfaces ==="
echo ""

# Parse and display
echo "$ip_output" | awk '
BEGIN {
    current_iface = ""
    inet_count = 0
}

# New interface line (starts with digit)
/^[0-9]+:/ {
    if (current_iface != "") {
        print ""
    }
    # Extract interface name
    split($2, parts, ":")
    current_iface = parts[1]

    # Get state (UP/DOWN)
    state = "DOWN"
    for (i = 3; i <= NF; i++) {
        if ($i == "UP") {
            state = "UP"
            break
        }
    }

    printf "Interface: %s [%s]\n", current_iface, state
    inet_count = 0
}

# IPv4 address
/inet [0-9]/ && !/inet6/ {
    inet_count++
    split($2, addr_parts, "/")
    printf "  IPv4 #%d: %s\n", inet_count, addr_parts[1]
}

# IPv6 address
/inet6/ {
    split($2, addr_parts, "/")
    # Skip link-local and loopback for cleaner output
    if (addr_parts[1] !~ /^fe80:/ && addr_parts[1] !~ /^::1/) {
        printf "  IPv6: %s\n", addr_parts[1]
    }
}
'

echo ""
echo "=== Statistics ==="
echo ""

if [[ -n "$INTERFACE" ]]; then
    # Show stats for specific interface
    echo "$INTERFACE:"
    cat /proc/net/dev | grep "$INTERFACE" | awk '{
        printf "  RX: %s bytes, %s packets\n", $2, $3
        printf "  TX: %s bytes, %s packets\n", $10, $11
    }'
else
    # Show summary stats
    cat /proc/net/dev | tail -n +3 | awk '{
        total_rx += $2
        total_tx += $10
    }
    END {
        printf "Total RX: %s bytes\n", total_rx
        printf "Total TX: %s bytes\n", total_tx
    }'
fi

exit 0
