# import socket library
import socket
import csv
from pandas import read_csv      
# import threading library
import threading
header = ['name', 'message']
#creat dtabase file
with open("data.csv", "w+", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(header) # write the header
# Choose a port that is free
PORT = 5000
key=[]
# An IPv4 address is obtained
# for the server.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
SERVER = s.getsockname()[0]
s.close()


# Address is stored as a tuple
ADDRESS = (SERVER, PORT)

# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

# Lists that will contains
# all the clients connected to
# the server and their names.
clients, names = [], []

# Create a new socket for
# the server
server = socket.socket(socket.AF_INET,
					socket.SOCK_STREAM)

# bind the address of the
# server to the socket
server.bind(ADDRESS)

# function to start the connection
def startChat():

	print("server is working on " + SERVER)
	
	# listening for connections
	server.listen()
	
	while True:
	
		# accept connections and returns
		# a new connection to the client
		# and the address bound to it
		conn, addr = server.accept()
		conn.send("INFO".encode(FORMAT))
		
		# 1024 represents the max amount
		# of data that can be received (bytes)
		info = conn.recv(10240).decode(FORMAT).split('+')
		name=info[0]
		key.append(info[1].encode(FORMAT))
		# append the name and client
		# to the respective list
		names.append(name)
		clients.append(conn)
		if len(key)==2:
			clients[0].send(key[1])
			clients[1].send(key[0])
		print(f"Name is :{name}")
		
		# broadcast message
		# broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
		
		# conn.send('Connection successful!'.encode(FORMAT))
		
		# Start the handling thread
		thread = threading.Thread(target = handle,
								args = (conn, addr))
		thread.start()
		
		# no. of clients connected
		# to the server
		print(f"active connections {threading.activeCount()-1}")

# method to handle the
# incoming messages
def handle(conn, addr):

	print(f"new connection {addr}")
	connected = True
	
	while connected:
		# receive message
		message = conn.recv(1024)
		msg=message.decode(FORMAT).replace(': ',',')
		with open('data.csv','a') as f: 
				f.write(msg)
				f.write('\n')
		# broadcast message
		index = clients.index(conn)
		if index:
			clients[0].send(message)
		else:
			clients[1].send(message)
        
	
	# close the connection
	conn.close()

# method for broadcasting
# messages to the each clients
# def broadcastMessage(message):
# 	for client in clients:
#          client.send(message)

# call the method to
# begin the communication
startChat()
