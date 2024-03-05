import socket
import csv 
from cryptography.fernet import Fernet
from student import Student

# Define host and port
HOST = 'localhost'  # Localhost
PORT = 12345        # Port to listen on

# Create a socket object
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_sock.bind((HOST, PORT))
server_sock.listen()

print('Server is listening for connections...')

# Accept a connection
client_sock, addr = server_sock.accept()
print('Connected to client:', addr)


def record_student_names_from_csv(csv_filename):
    students = {}
    Lab_avg = {}
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)       
        for row in csvreader:
            student = Student.from_csv_row(row)
            students[student.student_id]=student
            Lab_avg["lab1"] = Lab_avg.get("lab1",0) + student.lab1
            Lab_avg["lab2"] = Lab_avg.get("lab2",0) + student.lab2
            Lab_avg["lab3"] = Lab_avg.get("lab3",0) + student.lab3
            Lab_avg["lab4"] = Lab_avg.get("lab4",0) + student.lab4
    return students,Lab_avg


csv_filename = 'course_grades_2024.csv' 
students,Lab_avg = record_student_names_from_csv(csv_filename)
Lab_avg["lab1"] = Lab_avg["lab1"]/len(students)
Lab_avg["lab2"] = Lab_avg["lab2"]/len(students)
Lab_avg["lab3"] = Lab_avg["lab3"]/len(students)
Lab_avg["lab4"] = Lab_avg["lab4"]/len(students)

# Receive commands from client
while True:
    # Receive data from the client
    data = client_sock.recv(1024)
    
    # If no data is received, the client has closed the connection
    if not data:
        print('Client has closed the connection.')
        break
    
    # Decode the received data (assuming it's encoded as UTF-8)
    command = data.decode('utf-8')
    cmd,id = command.split(" ")


    if (cmd in ['GMA','GL1A','GL2A','GL3A','GL4A','GEA','GG']) and (id in students.keys()):

        # Form fernet key from student key
        encryption_key_bytes = students[id].key.encode('utf-8')
        fernet = Fernet(encryption_key_bytes)

        if cmd == 'GMA':
            print("Getting midterm average")
            output = str(students[str(id)].get_mt_avg())

        elif cmd == 'GL1A':
            print("Getting lab1 average")
            output = str(Lab_avg["lab1"])

        elif cmd == 'GL2A':
            print("Getting lab2 average")
            output = str(Lab_avg["lab2"])

        elif cmd == 'GL3A':
            print("Getting lab3 average")
            output = str(Lab_avg["lab3"])

        elif cmd == 'GL4A':
            print("Getting lab4 average")
            output = str(Lab_avg["lab4"])

        elif cmd == 'GEA':
            print("Getting exam average")
            output = str(students[str(id)].get_exam_avg())

        elif cmd == 'GG':
            print("Getting grades")
            output = str(students[str(id)].get_grades())

        output = fernet.encrypt(output.encode('utf-8'))
        client_sock.sendall(output)

    else:
        if cmd not in ['GMA','GL1A','GL2A','GL3A','GL4A','GEA','GG']:
            output = 'Invalid command'
        elif id not in students.keys():
            output = 'Invalid student ID ' + id
            
        else:
            output = 'Invalid command'

        client_sock.sendall(output.encode('utf-8'))
        client_sock.close()
        server_sock.listen()
        client_sock, addr = server_sock.accept()
        print('Connected to client:', addr)
    # Process the command (in this example, just print it)
    print('Received command from client:', command)

# Close the client socket
client_sock.close()

# Close the server socket
server_sock.close()