# Uncomment this to pass the first stage
import socket as s
import sys
import gzip

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
        request_line = data.split("\r\n")[0]
        headers_and_body = data.split("\r\n\r\n", 1)
        headers = headers_and_body[0]
        body = headers_and_body[1] if len(headers_and_body) > 1 else ""
        method, path, _ = request_line.split(" ")
        if method == "POST" and path.startswith("/files"):
            direc =sys.argv[2].rstrip('/')
            filename = path[7:]
            full_path = f"{direc}/{filename}"
            try:
                with open(full_path, "x") as f:
                    f.write(body)
                connection.send(b"HTTP/1.1 201 Created\r\n\r\n")
            except FileExistsError:
                connection.send(b"HTTP/1.1 409 Conflict\r\n\r\n")
            except:  
                connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        elif path.startswith("/files"):
            try:
                filename = path[7:] 
                direc = sys.argv[2].rstrip('/') 
                full_path = f"{direc}/{filename}"
                print(f"Trying to open: {full_path}")
                with open(full_path, "r") as f:
                    body = f.read()
                length = str(len(body)).encode("utf-8")
                response = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Type: application/octet-stream\r\n"
                    b"Content-Length: " + length + b"\r\n"
                    b"\r\n" + body.encode("utf-8")
                )
                connection.send(response)
            except:
                connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
        elif path.startswith("/echo"):
            headerss = data.split("\r\n")
            st = path.split("/")[-1].encode("utf-8")
            length = str(len(st)).encode("utf-8")
            encod_type = ""
            for header in headerss:
                if header.startswith("Accept-Encoding:"):
                    encod_type = header.split(": ", 1)[1]
                    break
            if "gzip" in encod_type.split(", "):
                comp = gzip.compress(st.encode(""))
                length = str(len(comp)).encode("utf-8")
                response = (
                    b"HTTP/1.1 200 OK\r\n"
                    b"Content-Encoding: gzip\r\n"
                    b"Content-Type: text/plain\r\n"
                    b"Content-Length: " + length + b"\r\n"
                    b"\r\n" + comp
                )
            else:
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
