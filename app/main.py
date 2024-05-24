# Uncomment this to pass the first stage
import socket as s
import sys
import os

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = s.create_server(("localhost", 4221))
    server_socket.listen()  
    # Uncomment this to pass the first stage
    while True: 
        connection , address = server_socket.accept()
        print(f"Connected by {address}")
        data = connection.recv(4096).decode("utf-8")
        path = data.split(" ")[1]
        if path.startswith("/files"):
            try:
                filename = path.split("/")[-1].encode("utf-8") 
                print(filename)
                direc = sys.argv[2]
                with open(f"/{direc}/{filename}", "r") as f:
                    body = f.read()
                length = str(len(body)).encode("utf-8")   
                response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: application/octet-stream\r\n"
                b"Content-Length" + length + b"\r\n"
                b"\r\n"  + body
                )
                connection.send(response)
            except:
                connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        elif path.startswith("/echo"):
            st = path.split("/")[-1].encode("utf-8")
            length = str(len(st)).encode("utf-8")
            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: " + length + b"\r\n"
                b"\r\n" + st
            )
            connection.send(response)
        elif path == "/user-agent":
            headers = data.split("\r\n")
            agent = ""
            for header in headers:
                if header.startswith("User-Agent:"):
                    agent = header.split(": ", 1)[1].encode("utf-8")
                    break
            length = str(len(agent)).encode("utf-8")
            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain\r\n"
                b"Content-Length: " + length + b"\r\n"
                b"\r\n" + agent
            )     
            connection.send(response)
        elif path == "/":
            connection.send(b"HTTP/1.1 200 OK\r\n\r\n")
        else:
            connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")         


if __name__ == "__main__":
    main()
