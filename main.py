import time

from remote_reader import (
    read_new_events,
    save_offset
)
from hec_client import send_event

POLL_INTERVAL = 5

def main():

    print("======================================")
    print(" Suricata → Splunk SOC Collector")
    print("======================================")

    while True:

        try:

            events, new_offset = read_new_events()

            all_successful = True

            for event in events:

                success = send_event(event)

                if success:

                    print(
                        "Event sent to Splunk:",
                        event.get("event_type")
                    )

                else:

                    print(
                        "Failed to send event."
                    )

                    all_successful = False

            if all_successful:

                save_offset(new_offset)
                print(
                    f"Offset updated to: {new_offset}"
                )
            else:

                print(
                    "Offset not updated due to send failures."
                )

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:

            print("\nCollector stopped.")

            break

        except Exception as error:

            print(
                "Collector error:",
                error
            )

            print(
                "Retrying in 5 seconds..."
            )

            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()