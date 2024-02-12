
import os

FORMAT = "utf-8"
def lengthen_message(message):
    return b' '* (1024 - len (message)) + message.encode(FORMAT)

def send_message(message, sockett):

    print(len (message))
    print(len(message)//262144)
    length = b' '* (1024 - len (message)) + str(len(message)).encode(FORMAT)
    sockett.sendall(length)                       # send the length of the message
    i=0
    for lines in range(0, len(message), 262144): 
        if i%100 == 0:
            print(i)
        i+=1
        outputData = message[lines:lines+262144]
        sockett.sendall(outputData)

        

def receive_message(sockett):
 
    data_length = sockett.recv(262144).decode(FORMAT).strip()
    data_length = int(data_length)
    output = b""
    while(data_length>0):
        recieve = sockett.recv(262144) 
        output += recieve
        data_length -=len(recieve)
            
    return output
        

def send_file(filename,sockett):
    
    if os.path.isfile(filename):
        sockett.sendall(lengthen_message("ClientHasFile"))
        c_status = sockett.recv(1024).decode(FORMAT).strip()
        if c_status == "Approved":
            try:
                with open(filename, 'rb') as file:
                        
                        data_of_file = file.read()
                send_message(data_of_file, sockett)                # send the contents of the file
                #reports
                print()
                sockett.sendall(lengthen_message("[SENDER] File copied and sent successfully!"))
                print("[SENDER] Binary file copied and sent successfully!")
                print(sockett.recv(1024).decode(FORMAT).strip())


            except FileNotFoundError:

                print()
                print("[SENDER] File not found.")
                print()
                sockett.sendall(lengthen_message("FileNotFound"))

        elif c_status == "FileExists":
            print("[RECEIVER] File already exists")
    else:
        print("[SENDER] No such file found")
        sockett.sendall(lengthen_message("FileNotFound"))




def receive_file(filename, sockett): 

    clientHasFile = sockett.recv(1024).decode(FORMAT).strip()
    if clientHasFile == "ClientHasFile":
        if os.path.isfile(filename):
            sockett.sendall(lengthen_message("FileExists"))
            print("[RECEIVER] File already exists")

        else:
            sockett.sendall(lengthen_message("Approved"))

            data_of_file = receive_message(sockett)                # recieve the contents of the file
            if data_of_file != "FileNotFound":      # check if file was sent

                try:    

                    with open(filename, "xb") as file:

                        file.write(data_of_file)                   # create a file and write in it 
                    
                    #reports
                    print(sockett.recv(1024).decode(FORMAT).strip())       
                    sockett.sendall(lengthen_message("[RECEIVER] File created, information saved in file"))
                    print("[RECEIVER] File created, information saved in file")
                    print()


                except FileExistsError:

                    print(sockett.recv(1024).decode(FORMAT).strip())
                    print("[RECEIVER] File already exists")
                    print()
                    sockett.sendall(lengthen_message("[RECEIVER] File already exists"))
            
            else:
                print()
                print("[SERVER] File not found, try a different filename")
                print()
    else:
        print("[SENDER] No such file found")

       
