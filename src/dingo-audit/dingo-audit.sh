#!/bin/bash
# dingo-audit: Quick vulnerability scan & forensic check
# Part of Dingo OS v1 - Network security utility

set -e

VERSION="1.0"
VERBOSE=false
OUTPUT_FILE=""

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    cat << EOF
dingo-audit v${VERSION} - Quick Network Vulnerability & Forensic Scanner

USAGE:
    dingo-audit [OPTIONS]

OPTIONS:
    --help              Show this help message
    --verbose           Verbose output
    --output FILE       Save report to file
    --network           Scan local network
    --system            Scan local system
    --all               Scan both network and system
    --quick             Quick scan (default)

EXAMPLES:
    dingo-audit --quick              # Quick local scan
    dingo-audit --all                # Full scan (network + system)
    dingo-audit --system --verbose   # Detailed system audit
    dingo-audit --network --output report.txt

EOF
}

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  Dingo-Audit v${VERSION} - Security Scanner   ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    echo -e "${YELLOW}→ $1${NC}"
}

print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
    fi
}

# System Audit Functions
audit_open_ports() {
    print_section "Scanning open ports..."

    if command -v ss &> /dev/null; then
        ss -tlnp 2>/dev/null | grep LISTEN || echo "No listening ports found"
    elif command -v netstat &> /dev/null; then
        netstat -tlnp 2>/dev/null | grep LISTEN || echo "No listening ports found"
    else
        echo "ss or netstat not found - skipping port scan"
    fi
}

audit_running_services() {
    print_section "Checking running services..."

    systemctl list-units --type=service --state=running 2>/dev/null | head -20 || \
        ps aux | grep -v grep | head -10
}

audit_file_permissions() {
    print_section "Checking critical file permissions..."

    for file in /etc/passwd /etc/shadow /etc/sudoers /root/.ssh; do
        if [ -e "$file" ]; then
            perms=$(ls -l "$file" | awk '{print $1}')
            echo "  $file: $perms"
        fi
    done
}

audit_user_accounts() {
    print_section "Checking user accounts..."

    echo "System users:"
    cat /etc/passwd | awk -F: '$3 >= 1000 {print "  " $1 " (UID: " $3 ")"}' || echo "  No additional users"

    echo ""
    echo "Sudoers:"
    sudo -l -U root 2>/dev/null | head -5 || echo "  (requires sudo access)"
}

audit_network_interfaces() {
    print_section "Checking network interfaces..."

    if command -v ip &> /dev/null; then
        ip addr show | grep -E "inet|inet6" || echo "No IP addresses found"
    else
        ifconfig | grep -E "inet|inet6" || echo "ifconfig not found"
    fi
}

audit_open_connections() {
    print_section "Checking active network connections..."

    if command -v ss &> /dev/null; then
        ss -tnp 2>/dev/null | head -10 || echo "No connections found"
    elif command -v netstat &> /dev/null; then
        netstat -tnp 2>/dev/null | head -10 || echo "No connections found"
    fi
}

audit_firewall() {
    print_section "Checking firewall status..."

    if command -v ufw &> /dev/null; then
        ufw status 2>/dev/null || echo "UFW not active"
    elif command -v iptables &> /dev/null; then
        iptables -L -n 2>/dev/null | head -5 || echo "Iptables not accessible"
    else
        echo "No firewall tools found"
    fi
}

audit_installed_packages() {
    print_section "Checking installed packages (security updates)..."

    apt list --upgradable 2>/dev/null | head -10 || echo "No upgrade info available"
}

audit_system_logs() {
    print_section "Recent system logs (errors/warnings)..."

    journalctl -p err -n 5 2>/dev/null || tail -5 /var/log/syslog 2>/dev/null || echo "Cannot access logs"
}

# Network Scan Functions
network_scan() {
    print_section "Network scanning (requires root)..."

    if ! command -v nmap &> /dev/null; then
        echo "nmap not installed - skipping network scan"
        echo "Install with: sudo apt install nmap"
        return
    fi

    # Get local network
    local_ip=$(hostname -I | awk '{print $1}')
    network="${local_ip%.*}.0/24"

    echo "Scanning network: $network"
    echo "(This may take a minute...)"

    sudo nmap -sP "$network" 2>/dev/null || echo "Network scan requires elevated privileges"
}

network_connections() {
    print_section "Network connections scan..."

    if command -v ss &> /dev/null; then
        echo "All network connections:"
        ss -tnpa 2>/dev/null | head -15 || echo "No connections found"
    fi
}

# Main execution
generate_report() {
    local report=""

    report+="$(date)\n"
    report+="Dingo-Audit Report\n"
    report+="==================\n\n"

    # System info
    report+="System Information:\n"
    report+="$(uname -a)\n"
    report+="$(lsb_release -d)\n\n"

    # Capture audit output
    report+="$(audit_open_ports 2>&1)\n"
    report+="$(audit_user_accounts 2>&1)\n"

    if [ ! -z "$OUTPUT_FILE" ]; then
        echo -e "$report" > "$OUTPUT_FILE"
        echo -e "${GREEN}Report saved to: $OUTPUT_FILE${NC}"
    fi
}

# Parse arguments
SCAN_TYPE="quick"

while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            show_help
            exit 0
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --network)
            SCAN_TYPE="network"
            shift
            ;;
        --system)
            SCAN_TYPE="system"
            shift
            ;;
        --all)
            SCAN_TYPE="all"
            shift
            ;;
        --quick)
            SCAN_TYPE="quick"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main execution
print_header

case $SCAN_TYPE in
    quick)
        echo "Running QUICK SCAN..."
        echo ""
        audit_open_ports
        echo ""
        audit_file_permissions
        echo ""
        audit_user_accounts
        ;;
    system)
        echo "Running SYSTEM AUDIT..."
        echo ""
        audit_open_ports
        echo ""
        audit_running_services
        echo ""
        audit_file_permissions
        echo ""
        audit_user_accounts
        echo ""
        audit_firewall
        echo ""
        audit_installed_packages
        echo ""
        audit_system_logs
        ;;
    network)
        echo "Running NETWORK SCAN..."
        echo ""
        audit_network_interfaces
        echo ""
        audit_open_connections
        echo ""
        network_scan
        echo ""
        network_connections
        ;;
    all)
        echo "Running FULL AUDIT (system + network)..."
        echo ""
        audit_open_ports
        echo ""
        audit_running_services
        echo ""
        audit_file_permissions
        echo ""
        audit_user_accounts
        echo ""
        audit_network_interfaces
        echo ""
        audit_open_connections
        echo ""
        audit_firewall
        echo ""
        audit_installed_packages
        echo ""
        audit_system_logs
        echo ""
        network_scan
        ;;
esac

echo ""
echo -e "${BLUE}Scan complete!${NC}"

if [ ! -z "$OUTPUT_FILE" ]; then
    generate_report
fi
