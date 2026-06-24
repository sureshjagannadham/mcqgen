
## 🚀 AWS EC2 Deployment Guide

Follow these step-by-step instructions to configure your Ubuntu server and host the Streamlit application.

### 1. AWS Instance Setup
* Log in to the [AWS Management Console](https://amazon.com).
* Search for **EC2** in the search bar.
* Launch a new instance using the **Ubuntu** OS image.

### 2. Configure Security Groups (Inbound Rules)
* Go to your running instance security settings.
* Click on **Edit inbound rules**.
* Add a **Custom TCP** rule.
* Set the port range to `8501`.
* Set the source to `0.0.0.0/0` (Anywhere).

### 3. Server Configuration & Package Installation
Connect to your EC2 instance via SSH and run the following commands to update the system:

```bash
# Update the package lists
sudo apt update
sudo apt-get update

# Upgrade installed packages
sudo apt upgrade -y

# Install core utilities
sudo apt install git curl unzip tar make sudo vim wget -y

# Install Python package manager
sudo apt install python3-pip -y
```

### 4. Clone Repository & Install Requirements
```bash
# Clone your project code
git clone <Your-Repository-URL>

# Navigate into the project folder
cd mcqgen

# Install project dependencies
pip3 install -r requirements.txt
```

### 5. Configure Environment Variables
Create a hidden environment file to store your OpenAI API secret key safely:

```bash
# Create the environment file
touch .env

# Open the file using Vim editor
vi .env
```
* Press `i` to enter Insert Mode.
* Paste your credentials: `OPENAI_API_KEY=your_actual_api_key`
* Press `Esc`, then type `:wq` and hit `Enter` to save and exit.

### 6. Run the Application
```bash
python3 -m streamlit run StreamlitAPP.py
```