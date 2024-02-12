import socket
import sys
import os

sys.path.insert(1, os.path.dirname(os.getcwd()))

import mymodule as m


FORMAT = "utf-8"

def start(): # main fumction

    
    server = connect()
    server.listen()

    while True: 
        client_socket, client_address = server.accept()
        print()
        print(f"CLIENT {client_address} CONNECTED")      
        print()
        handle(client_socket)
        
        

def handle(client_socket): # handling requests

    command = client_socket.recv(1024).decode(FORMAT).strip()                           # receive the command

    if command == "NoCommandGiven":                                         # check if command was given from the client's side
        print("[SERVER] No command was given")
        return None
    
    if (command == "list"):

        dir_list = os.listdir()                                             # get the directory contents
        m.send_message(",".join(dir_list).encode(FORMAT), client_socket)         # send it
        print("[SENDER] The directory contents are sent.")                  # report
        
    else:

        filename = client_socket.recv(1024).decode(FORMAT).strip()     # receive the filename
        if filename != "FilenameUnknown":
        
            if (command == "put"):

                m.receive_file(filename, client_socket)                         # recieve the file


            elif (command == "get"):

                m.send_file(filename, client_socket)                            # send the file
                
        
        else:

            print("[SERVER] Command umknown or no filename given")                               # report unrecognised command
            client_socket.sendall(m.lengthen_message("[SERVER] Command umknown"))
            
        
        

def connect():                                                              # creating a socket, registering with OS

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
    server.bind(("", int(sys.argv[1])))

    print('SERVER UP AND RUNNING')

    return server

     


start()
