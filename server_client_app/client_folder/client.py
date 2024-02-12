import socket
import sys
import os

sys.path.insert(1, os.path.dirname(os.getcwd()))
import mymodule as m

FORMAT = "utf-8"

def start(): # main fumction

    while True:
        client = connect()
        message = sys.argv[3:]
        if message == []:
            print("[CLIENT] No command given")
            client.sendall(m.lengthen_message("NoCommandGiven"))
            sys.exit()
        handle(message, client)
        client.close()
        


def connect():                                                  # create a socket, connect it to the sercer 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((sys.argv[1], int(sys.argv[2]))) 
    return client



def handle(message, sockett):                                   # handling the requests

    command = message[0]
               
    sockett.sendall(m.lengthen_message(command))                   # send the request to server

    if  (command == 'list'):
        
        names_of_files = m.receive_message(sockett).decode(FORMAT).split(",")      # receive the contents of directory 

        for name in names_of_files:                                             # print it out
            print(name)
                
        print()

        sys.exit()
        
    else:
        

        if (len(message)>1):

            filename = message[1]
            sockett.sendall(m.lengthen_message(filename))                    # send the filename

            
            if (command == "put"):

                print()                
                m.send_file(filename, sockett)                                  # send the contents of the file
                print()

                sys.exit()


            elif (command == "get"):

                print()
                m.receive_file(filename, sockett)                               # receive the contents of the file
                print()

                sys.exit()



        else:
            print()
            print("[CLIENT] Command unknown or no filename given")
            sockett.sendall(m.lengthen_message("FilenameUnknown"))
            print()

            sys.exit()

    
start()
