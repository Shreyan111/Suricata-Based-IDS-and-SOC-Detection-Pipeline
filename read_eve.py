import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

ubuntu_host = os.getenv("UBUNTU_HOST")
ubuntu_user = os.getenv("UBUNTU_USER")
ubuntu_password = os.getenv("UBUNTU_PASSWORD")
eve_path = os.getenv("UBUNTU_EVE_PATH")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print("Connecting to Ubuntu...")

    ssh.connect(
        hostname=ubuntu_host,
        username=ubuntu_user,
        password=ubuntu_password
    )

    print("Connected to Ubuntu.")

    sftp = ssh.open_sftp()

    print("Opening:", eve_path)

    with sftp.open(eve_path, "r") as remote_file:

        # Read the last 10 lines
        lines = remote_file.readlines()[-10:]

        print("\nLast 10 EVE JSON events:\n")

        for line in lines:
            print(line.strip())

    sftp.close()

finally:
    ssh.close()