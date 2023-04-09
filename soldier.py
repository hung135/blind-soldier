import socket
import struct
import threading
import json

MULTICAST_GROUP = '224.0.0.1'
PORT = 12345

class Soldier:
    def __init__(self, ip, name, task_list):
        self.ip = ip
        self.name = name
        self.task_list = task_list
        self.peers = {}
        self.task_assignment = {self.name: task_list}

    def new_peer(self, name, ip):
        self.peers[name] = ip
        self.divide_tasks()

    def remove_peer(self, name):
        if name in self.peers:
            del self.peers[name]
            self.divide_tasks()

    def divide_tasks(self):
        all_tasks = [task for tasks in self.task_assignment.values() for task in tasks]
        num_peers = len(self.peers) + 1
        tasks_per_peer, remainder = divmod(len(all_tasks), num_peers)

        task_assignments = {}
        task_index = 0

        for peer_name in [self.name, *self.peers.keys()]:
            num_tasks = tasks_per_peer + (1 if remainder > 0 else 0)
            task_assignments[peer_name] = all_tasks[task_index : task_index + num_tasks]
            task_index += num_tasks
            remainder -= 1

        self.task_assignment = task_assignments

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
