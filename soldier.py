import socket
import struct
import threading
import time
import json
import argparse

MULTICAST_GROUP = '224.0.0.1'
PORT = 12345

class Soldier:
    def __init__(self, ip, name, task_list):
        self.ip = ip
        self.name = name
        self.task_list = task_list
        self.peers = []
        self.task_assignment = {self.name: task_list}

    def new_peer(self, name, ip):
        self.peers.append((name, ip))
        self.divide_tasks()

    def remove_peer(self, name):
        self.peers = [peer for peer in self.peers if peer[0] != name]
        self.divide_tasks()

    def divide_tasks(self):
        all_tasks = self.task_list.copy()
        for _, tasks in self.task_assignment.items():
            all_tasks.extend(tasks)

        num_peers = len(self.peers) + 1
        num_tasks_per_peer = len(all_tasks) // num_peers

        self.task_assignment = {self.name: all_tasks[:num_tasks_per_peer]}
        for i, (name, _) in enumerate(self.peers):
            start = (i + 1) * num_tasks_per_peer
            end = (i + 2) * num_tasks_per_peer
            self.task_assignment[name] = all_tasks[start:end]

        print(f"{self.name}'s Task Assignments: {self.task_assignment}")

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))
            s.sendto(json.dumps(message).encode(), (MULTICAST_GROUP, PORT))

    def receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', PORT))

            group = socket.inet_aton(MULTICAST_GROUP)
            mreq = struct.pack('4sL', group, socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            while True:
                data, _ = s.recvfrom(1024)
                if data:
                    message = json.loads(data.decode())
                    if message["action"] == "new_peer" and message["ip"] != self.ip:
                        self.new_peer(message["name"], message["ip"])
                    elif message["action"] == "remove_peer" and message["name"] != self.name:
                        self.remove_peer(message["name"])

    def listen(self):
        threading.Thread(target=self.receive_message).start()

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
    main(args
