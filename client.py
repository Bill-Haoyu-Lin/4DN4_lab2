import socket
from cryptography.fernet import Fernet
import csv
from student import Student

# Define host and port
HOST = 'localhost'  # Server's IP address (localhost in this case)
PORT = 12345        # Port on which server is listening

# Create a socket object
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_sock.connect((HOST, PORT))

def record_student_names_from_csv(csv_filename):
    students = {}
    with open(csv_filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            student = Student.from_csv_row(row)
            students[student.student_id]=student
    return students

csv_filename = 'course_grades_2024.csv'  # replace 'students.csv' with your CSV file name
students = record_student_names_from_csv(csv_filename)



# Send commands to the server
while True:
    # Get input command from user
    command = input('Enter command: ')

    if command.lower() == 'exit':
        break

    # Send the command to the server
    student_id = command.split(" ")[1]
    client_sock.sendall(command.encode('utf-8'))
    

    data = client_sock.recv(1024)

    if data and student_id in students.keys():
        print('Received data from server:', data)
        encryption_key_bytes = students[student_id].key.encode('utf-8')
        fernet = Fernet(encryption_key_bytes)
        decrypted_message_bytes = fernet.decrypt(data)
        decrypted_message = decrypted_message_bytes.decode('utf-8')
        print("decrypted_message = ", decrypted_message)
    elif data:
        print('Received data from server:', data.decode('utf-8'))


    # If the user enters "exit", close the connection
    
   

# Close the client socket
client_sock.close()