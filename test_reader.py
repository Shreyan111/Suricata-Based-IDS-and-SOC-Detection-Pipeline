from remote_reader import read_new_events


events = read_new_events()


for event in events:

    print("\n-----------------------------")

    print("Event Type:", event.get("event_type"))

    print("Source IP:", event.get("src_ip"))

    print("Destination IP:", event.get("dest_ip"))

    print("Protocol:", event.get("proto"))

    print("Alert:", event.get("alert"))

    print("-----------------------------")