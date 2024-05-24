# Uncomment this to pass the first stage
import socket as s


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    # Uncomment this to pass the first stage
    #
    server_socket = s.create_server(("localhost", 4221))
    server_socket.listen()
    connection , address = server_socket.accept()
    data = connection.recv(4096).decode("utf-8")
    path = data.split(" ")[1]
    if path.startswith("/echo"):
        st = path.split("/")[-1].encode("utf-8")
        length = str(len(st)).encode("utf-8")
        response = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: " + length + b"\r\n"
            b"\r\n" + st
        )
        connection.send(response)
    else:
        connection.send(b"HTTP/1.1 404 Not Found\r\n\r\n") 


if __name__ == "__main__":
    main()
