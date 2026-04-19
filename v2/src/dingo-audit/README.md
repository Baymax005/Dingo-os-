# dingo-audit - Network Vulnerability & Forensic Scanner

Quick vulnerability assessment and forensic checks for Dingo OS networks.

## Features

- **Quick Scan** - Fast port and permission check
- **System Audit** - Deep system security review
- **Network Scan** - Local network enumeration
- **Full Audit** - Complete system + network assessment
- **Forensic Checks** - File permissions, user accounts, recent logs

## Usage

```bash
# Quick scan (default)
./dingo-audit.sh

# Full system audit
./dingo-audit.sh --system

# Network scan
./dingo-audit.sh --network --verbose

# Complete scan with output to file
./dingo-audit.sh --all --output audit-report.txt

# Help
./dingo-audit.sh --help
```

## Checks Performed

### System Audit
- Open ports and listening services
- Running services status
- Critical file permissions (/etc/passwd, /etc/shadow, /etc/sudoers)
- User accounts and sudoers
- Firewall configuration
- Available security updates
- Recent system logs

### Network Scan
- Network interfaces and IPs
- Active connections
- Local network enumeration (requires nmap)
- Connection details

## Requirements

- Linux (Debian/Ubuntu based)
- ss or netstat (for port checking)
- systemctl (for service checks)
- Optional: nmap (for network scanning)
- Optional: ufw or iptables (for firewall info)

## Output

Default: Console output
Optional: Save to file with `--output filename.txt`

## Future Enhancements (v2)

- Database logging
- Alert thresholds
- Automatic remediation
- Integration with monitoring systems
- Custom rule creation
