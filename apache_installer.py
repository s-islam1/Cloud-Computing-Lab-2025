#!/usr/bin/env python3
"""
Simple helper to install and start Apache (httpd / apache2) on a Linux EC2 instance.
Usage:
    - Dry run (show steps): python apache_installer.py
    - Apply (perform installation): python apache_installer.py --apply
Run this script on the EC2 instance (or copy it there) with root privileges (sudo) for --apply.
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

class ApacheInstaller:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.steps = []
        
    def log_step(self, description, command=None):
        """Log a step to be performed"""
        step_info = {"description": description, "command": command}
        self.steps.append(step_info)
        
        if self.dry_run:
            print(f"[DRY RUN] {description}")
            if command:
                print(f"  Command: {command}")
        else:
            print(f"[EXECUTING] {description}")
            if command:
                print(f"  Command: {command}")
    
    def run_command(self, command, description):
        """Execute a command if not in dry run mode"""
        self.log_step(description, command)
        
        if not self.dry_run:
            try:
                result = subprocess.run(
                    command, 
                    shell=True, 
                    check=True, 
                    capture_output=True, 
                    text=True
                )
                print(f"  ✓ Success: {result.stdout.strip()}")
                return result
            except subprocess.CalledProcessError as e:
                print(f"  ✗ Error: {e.stderr.strip()}")
                return None
        return True
    
    def check_system(self):
        """Check if running on Amazon Linux 2023"""
        self.log_step("Checking system version")
        
        if not self.dry_run:
            try:
                with open('/etc/system-release', 'r') as f:
                    release_info = f.read().strip()
                print(f"  System: {release_info}")
                
                if "Amazon Linux" not in release_info:
                    print("  ⚠ Warning: This script is optimized for Amazon Linux")
                    return True  # Still continue even if not Amazon Linux
                else:
                    print("  ✓ Amazon Linux detected - proceeding with installation")
                    return True  # Success case
                    
            except FileNotFoundError:
                print("  ⚠ Warning: Could not determine system version")
                return True  # Continue anyway
        
        return True  # Always return True for dry run mode
    
    def update_system(self):
        """Update system packages"""
        return self.run_command(
            "sudo dnf update -y",
            "Updating system packages"
        )
    
    def install_apache(self):
        """Install Apache web server"""
        return self.run_command(
            "sudo dnf install -y httpd",
            "Installing Apache web server (httpd)"
        )
    
    def start_apache(self):
        """Start Apache service"""
        return self.run_command(
            "sudo systemctl start httpd",
            "Starting Apache web server"
        )
    
    def enable_apache(self):
        """Enable Apache to start on boot"""
        return self.run_command(
            "sudo systemctl enable httpd",
            "Enabling Apache to start on boot"
        )
    
    def check_apache_status(self):
        """Check Apache service status"""
        return self.run_command(
            "sudo systemctl status httpd --no-pager",
            "Checking Apache service status"
        )
    
    def set_permissions(self):
        """Set proper permissions for web directory"""
        commands = [
            ("sudo usermod -a -G apache ec2-user", "Adding ec2-user to apache group"),
            ("sudo chown -R ec2-user:apache /var/www", "Changing ownership of /var/www"),
            ("sudo chmod 2775 /var/www", "Setting permissions on /var/www"),
            ("find /var/www -type d -exec sudo chmod 2775 {} \\;", "Setting directory permissions"),
            ("find /var/www -type f -exec sudo chmod 0664 {} \\;", "Setting file permissions")
        ]
        
        for command, description in commands:
            result = self.run_command(command, description)
            if not result and not self.dry_run:
                return False
        return True
    
    def create_test_page(self):
        """Create a simple test HTML page"""
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Apache Test Page</title>
</head>
<body>
    <h1>Apache Web Server is Running!</h1>
    <p>Congratulations! Your Apache web server is successfully installed and running on Amazon Linux 2023.</p>
    <p>Server time: <script>document.write(new Date());</script></p>
</body>
</html>'''
        
        self.log_step("Creating test HTML page", "echo 'HTML content' > /var/www/html/index.html")
        
        if not self.dry_run:
            try:
                with open('/var/www/html/index.html', 'w') as f:
                    f.write(html_content)
                print("  ✓ Test page created successfully")
                return True
            except Exception as e:
                print(f"  ✗ Error creating test page: {e}")
                return False
        return True
    
    def get_instance_info(self):
        """Get EC2 instance public IP/DNS"""
        self.log_step("Getting instance public IP address")
        
        if not self.dry_run:
            try:
                # Try to get public IP from instance metadata
                result = subprocess.run(
                    "curl -s http://169.254.169.254/latest/meta-data/public-ipv4",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout:
                    public_ip = result.stdout.strip()
                    print(f"  Public IP: {public_ip}")
                    print(f"  Test your server at: http://{public_ip}")
                    return True
                else:
                    print("  Could not retrieve public IP address")
                    return True  # Not a critical failure
            except Exception as e:
                print(f"  Error getting instance info: {e}")
                return True  # Not a critical failure
        return True
    
    def install_complete_setup(self):
        """Run the complete Apache installation process"""
        print("=" * 60)
        print("Apache Web Server Installation Script")
        print("=" * 60)
        
        if self.dry_run:
            print("DRY RUN MODE - No changes will be made")
            print("Use --apply flag to actually perform installation")
        else:
            print("INSTALLATION MODE - Changes will be applied")
            
            # Check if running as root or with sudo
            if os.geteuid() != 0:
                print("⚠ Warning: This script should be run with sudo privileges")
                print("Example: sudo python3 apache_installer.py --apply")
        
        print("-" * 60)
        
        # Execute installation steps
        steps = [
            self.check_system,
            self.update_system,
            self.install_apache,
            self.start_apache,
            self.enable_apache,
            self.set_permissions,
            self.create_test_page,
            self.check_apache_status,
            self.get_instance_info
        ]
        
        for step in steps:
            result = step()
            if not result and not self.dry_run:
                print(f"✗ Installation failed at step: {step.__name__}")
                return False
            print()
        
        print("=" * 60)
        if self.dry_run:
            print("DRY RUN COMPLETED")
            print("Run with --apply to perform actual installation")
        else:
            print("INSTALLATION COMPLETED SUCCESSFULLY!")
            print("Your Apache web server should now be running")
            print("Make sure your EC2 security group allows HTTP traffic on port 80")
        print("=" * 60)
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Install Apache web server on EC2 instance')
    parser.add_argument('--apply', action='store_true', 
                       help='Actually perform installation (default is dry run)')
    
    args = parser.parse_args()
    
    installer = ApacheInstaller(dry_run=not args.apply)
    installer.install_complete_setup()

if __name__ == "__main__":
    main()
