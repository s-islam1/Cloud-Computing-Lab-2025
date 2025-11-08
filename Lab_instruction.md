# 🚀 Apache Web Server Installation Guide (Amazon Linux 2023)

This guide provides a step-by-step process for using the `apache_installer.py` script to perform a complete, production-ready Apache HTTP Server installation on an **Amazon Linux 2023 EC2 instance**.

-----

## ⚙️ Prerequisites

  * An active **Amazon Linux 2023 EC2 Instance**.
  * The script, `apache_installer.py`, which is assumed to be in your current directory.
  * **SSH access** configured for your instance (including the necessary `.pem` key).

-----

## 🔒 Important: Security Group Configuration

Before running the script, ensure your EC2 instance's Security Group allows inbound **HTTP traffic** on port 80.

1.  Navigate to the **EC2 Console** $\rightarrow$ **Security Groups**.
2.  Select the Security Group associated with your EC2 instance.
3.  Add an **Inbound Rule**:
      * **Type:** `HTTP`
      * **Protocol:** `TCP`
      * **Port Range:** `80`
      * **Source:** `0.0.0.0/0` (Allows access from anywhere; restrict this to your specific IP range for better security.)

-----

## 📝 Step-by-Step Implementation Guide

### Step 1: Transfer the Script to Your EC2 Instance

You have two options for getting the `apache_installer.py` script onto your EC2 instance:

#### Option A: Create the File Directly (Recommended for quick setup)

Run these commands after connecting via SSH:

```bash
# Connect to your EC2 instance
ssh -i "your-key.pem" ec2-user@your-instance-public-dns

# Create the script file
nano apache_installer.py
```

  * Copy and paste the complete content of the `apache_installer.py` script.
  * Save and exit the editor (**Ctrl+X**, then **Y**, then **Enter**).

#### Option B: Transfer from Your Local Machine

If the script is already on your local machine, use `scp` (run this command from your **local machine**):

```bash
scp -i "your-key.pem" apache_installer.py ec2-user@your-instance-public-dns:~/
```

### Step 2: Make the Script Executable

Connect to your EC2 instance via SSH and run:

```bash
chmod +x apache_installer.py
```

### Step 3: Run a Dry Run (Highly Recommended)

Review the actions the script will take **without making any changes** to your system.

```bash
python3 apache_installer.py
```

### Step 4: Execute the Installation

Run the script with the `--apply` flag to perform the actual installation and configuration steps. This requires `sudo` privileges.

```bash
sudo python3 apache_installer.py --apply
```

### Step 5: Verify the Installation

The script will display the public IP address of your EC2 instance upon successful completion.

Open your web browser and navigate to:

```
http://your-instance-public-ip
```

You should see the test HTML page created by the script.

-----

## 📜 What the Script Does

The `apache_installer.py` script automates the following tasks to achieve a stable and ready-to-use Apache installation:

  * ✅ **System Check:** Verifies the operating system is **Amazon Linux 2023**.
  * 🔄 **Update System:** Runs a system update (`dnf update -y`).
  * ⬇️ **Install Apache:** Installs the `httpd` package.
  * ▶️ **Start Service:** Starts the Apache web server (`httpd`).
  * 🔁 **Enable Auto-start:** Configures Apache to start automatically on system boot.
  * 🔐 **Set Permissions:** Configures proper file permissions for the web root directory (`/var/www/html`).
  * 📄 **Create Test Page:** Generates a simple **HTML index page** for verification.
  * 🔍 **Status Check:** Confirms the Apache service is running.
  * 🖥️ **Display Info:** Outputs the **public IP address** for easy testing.

-----