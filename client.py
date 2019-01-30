# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port))
print(s.recv(1024))      

while True:
	command = raw_input()
	s.send(command.encode())
	if command == "killserver":
		print("Closing connection to the server!")
		# Close the connection with the server
		s.close()
		break
