import time
import argparse
from soldier import Soldier

def main(ip, name):
    tasks = [f"Task{str(i).zfill(2)}" for i in range(1, 21)]

    soldier = Soldier(ip, name, tasks)
    soldier.listen()

    time.sleep(1)

    soldier.send_message({"action": "new_peer", "name": soldier.name, "ip": soldier.ip})

    time.sleep(5)

    soldier.send_message({"action": "remove_peer", "name": soldier.name})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start a soldier process.")
    parser.add_argument("ip", type=str, help="IP address of the soldier")
    parser.add_argument("name", type=str, help="Name of the soldier")

    args = parser.parse_args()
    main(args.ip, args.name)
