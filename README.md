Blind Soldiers Task Management Protocol
Summary
The purpose of this protocol is to efficiently manage and distribute tasks among a group of blind soldiers (processes) in a dynamic environment. Each soldier, when spawned, will join the battlefield (multicast group) and start managing the tasks. As more soldiers enter the room, they coordinate amongst themselves and split up the tasks evenly. When a soldier gets killed or removed from the battlefield, the remaining soldiers will take over the missing soldier's tasks and continue to balance the workload.

Overview
The protocol is designed with the following key aspects:

Each soldier is represented by a process running on a separate machine, identified by their IP address and name.
Soldiers communicate and coordinate tasks through a multicast group, allowing efficient group communication.
When a soldier enters the battlefield, they join the multicast group and announce their presence to other soldiers.
Soldiers maintain a list of tasks and task assignments for themselves and their peers.
Tasks are divided evenly among all soldiers in the multicast group.
When a soldier leaves or is removed from the battlefield, the remaining soldiers take over the missing soldier's tasks and redistribute the workload evenly.
Soldiers continuously listen for messages from their peers to update task assignments and the list of soldiers in the battlefield.
Implementation
The protocol is implemented using Python and leverages the socket library to handle multicast communication between soldiers. Each soldier process can be spawned with command-line arguments to specify their IP address, name, and the multicast group to join.

Soldier Class
The Soldier class represents a blind soldier in the battlefield, responsible for managing tasks and coordinating with other soldiers in the multicast group.

Key attributes of the Soldier class include:

IP address and name
List of tasks
List of peers (other soldiers in the multicast group)
Task assignments for themselves and their peers
Key methods of the Soldier class include:

enter_room: Announce the soldier's presence and join the multicast group
new_peer: Add a new soldier to the list of peers and update task assignments
remove_peer: Remove a soldier from the list of peers and update task assignments
divide_tasks: Evenly distribute tasks among all soldiers in the multicast group
send_message: Send a message to the multicast group
receive_message: Receive and process messages from the multicast group
listen: Start listening for messages from other soldiers in the multicast group
Running the Protocol
To start a soldier process, run the script with the following command-line arguments:

bash
Copy code
python soldier.py <IP> <Name>
Replace <IP> with the IP address of the soldier's machine and <Name> with the desired name for the soldier.

When a soldier process starts, it joins the multicast group and begins managing tasks. Soldiers automatically balance the workload as they enter or leave the battlefield.
