import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

ubuntu_host = os.getenv("UBUNTU_HOST")
ubuntu_user = os.getenv("UBUNTU_USER")
ubuntu_password = os.getenv("UBUNTU_PASSWORD")

print("Ubuntu Host:", ubuntu_host)
print("Ubuntu User:", ubuntu_user)
print("Ubuntu Password:", ubuntu_password)

ssh = paramiko.SSHClient()

# Automatically accept the Ubuntu VM's SSH host key
# This is acceptable for a controlled lab environment.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting to Ubuntu...")
    ssh.connect(
        hostname=ubuntu_host,
        username=ubuntu_user,
        password=ubuntu_password
    )
    print("SSH connection successful!")

finally:
    ssh.close()