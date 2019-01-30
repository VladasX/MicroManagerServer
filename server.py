# Initialize MicroManager
MMDirectory = "C:\Program Files\Micro-Manager-2.0beta"

import socket
import datetime, time
from flask import Flask, redirect, url_for, render_template
from PIL import Image
import sys, traceback
sys.path.append(MMDirectory)
import MMCorePy


# Main program

print("starting MicroManager")
mmc = MMCorePy.CMMCore()

mmc.loadDevice('Camera', 'TimepixCamera', 'TimepixCam')
mmc.initializeAllDevices()
mmc.setCameraDevice('Camera')

	
def snap_image():
    try:
        mmc.snapImage()
        img = mmc.getImage()
        image_url = "images/" + datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f") + ".tiff"
        Image.fromarray(img).save(image_url)
        return True
    except : 
        traceback.print_exc()
        return False
	
	
### socket	

# next create a socket object 
s = socket.socket()          
print("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345                
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))         
print("Socket binded to port %s" % (port))
  
# put the socket into listening mode 
s.listen(1)      
print("Socket is listening")           
  
# Establish connection with client. 
c, addr = s.accept()      
print("Got connection from %s:%s" % (addr[0], addr[1]))

# send a thank you message to the client.  
c.send('Thank you for connecting'.encode())
  
print("Command usage: snap [frequency in seconds]")
while True: 
   
	command = c.recv(1024)
	if command.decode() == "killserver":
		print("%s Connection closed by the client" % datetime.datetime.now().strftime("[%H:%M:%S]"))
		# Close the connection with the client 
		c.close()
		break
	if command.decode()[:4] == "snap":
		args = command.split()
		if len(args) == 2:
			try:
				freq = float(args[1])
			except:
				print("Invalid command")
				continue
			print("Starting to snap images every %g seconds" % (freq))
			while True:
				if snap_image():
					print("%s Successfully snapped an image" % datetime.datetime.now().strftime("[%H:%M:%S]"))
				else:
					print("%s Could not snap an image, something went wrong!" % datetime.datetime.now().strftime("[%H:%M:%S]"))
				time.sleep(freq)
		else:
			if snap_image():
				print("%s Successfully snapped an image" % datetime.datetime.now().strftime("[%H:%M:%S]"))
			else:
				print("%s Could not snap an image, something went wrong!" % datetime.datetime.now().strftime("[%H:%M:%S]"))
