import json
import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

UBUNTU_HOST = os.getenv("UBUNTU_HOST")
UBUNTU_USER = os.getenv("UBUNTU_USER")
UBUNTU_PASSWORD = os.getenv("UBUNTU_PASSWORD")
EVE_PATH = os.getenv("UBUNTU_EVE_PATH")

STATE_FILE = "state/reader_state.json"

def load_offset():
    """
    Load the last processed byte offset.

    If no state exists, start from the beginning
    of the file.
    """

    if not os.path.exists(STATE_FILE):
        return 0

    with open(STATE_FILE, "r") as file:
        state = json.load(file)

    return state.get("offset", 0)


def save_offset(offset):
    """
    Save the current byte offset so that
    processing can continue from this position
    after the program restarts.
    """

    os.makedirs("state", exist_ok=True)

    with open(STATE_FILE, "w") as file:
        json.dump(
            {
                "offset": offset
            },
            file,
            indent=4
        )


def connect_ssh():
    """
    Create an SSH connection to Ubuntu.
    """

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy()
    )

    ssh.connect(
        hostname=UBUNTU_HOST,
        username=UBUNTU_USER,
        password=UBUNTU_PASSWORD
    )

    return ssh


def read_new_events():

    offset = load_offset()

    print("Last processed offset:", offset)

    ssh = connect_ssh()

    try:

        sftp = ssh.open_sftp()

        remote_file = sftp.open(EVE_PATH, "r")

        # Find the current size of eve.json
        file_size = remote_file.stat().st_size

        print("Current file size:", file_size)

        # Detect log rotation or truncation
        if file_size < offset:

            print(
                "File became smaller than the saved offset."
            )

            print(
                "Possible log rotation detected."
            )

            offset = 0

        # Move to the last processed position
        remote_file.seek(offset)

        new_events = []

        while True:

            line = remote_file.readline()

            if not line:
                break

            line = line.strip()

            if not line:
                continue

            try:

                event = json.loads(line)

                new_events.append(event)

            except json.JSONDecodeError:

                print(
                    "Incomplete JSON detected. "
                    "Stopping read for this cycle."
                )
                break

        # Save the new position
        new_offset = remote_file.tell()

        # save_offset(new_offset)

        remote_file.close()
        sftp.close()

        print(
            f"Read {len(new_events)} new events."
        )

        # print(
        #     f"New offset: {new_offset}"
        # )

        return new_events, new_offset

    finally:

        ssh.close()