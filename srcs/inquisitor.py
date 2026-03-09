#! /usr/bin/python3

import argparse
import socket, threading

def parser():
    parser = argparse.ArgumentParser(
        prog='inquisitor',
        description='ARP poisoning'
    )
    parser.add_argument(
        'SRC_IP',
        type=str,
        help="IP from source host"
    )
    parser.add_argument(
        'SRC_MAC',
        type=str,
        help="MAC from source host"
    )
    parser.add_argument(
        'TARGET_IP',
        type=str,
        help="IP from target host"
    )
    parser.add_argument(
        'TARGET_MAC',
        type=str,
        help="MAC from target host"
    )
    return parser.parse_args()


def handle_client(client_sock, client_address):
    while True:
        data = client_sock.recv(1024)
        if not data:
            print(f"Client desconected")
            client_sock.close()
            break
        message = data.decode('utf-8').strip()
        print(f"Readed: {message}")
        client_sock.send(f"Echo: {message}\n".encode('utf-8'))


if __name__ == "__main__":
    # parsed_args = parser()
    # print(parsed_args)
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    port = 8080
    print("hostname: ", hostname)
    print("name: ", host)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen(10)

    try:
        while True:
            client_sock, client_address = server_sock.accept()
            print(f"sock {client_sock} addr {client_address}")
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_sock, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_sock.close()
