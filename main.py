#!/usr/bin/env python
import argparse
import codecs
import socket


def hex_dump(data):
    for byte in data:
        in_hex = '\\x{:02x}'.format(byte)
        print(in_hex, end='')
    print(flush=True)

def handle_connection(sock, canned):
    data = None
    while(True):
        resp = canned.get(data)
        if resp:
            print('>', end='')
            hex_dump(resp)
            sock.send(resp)
            
        data = sock.recv(4096)
        if not data:
            break
        print('<', end='')
        hex_dump(data)


def do_client(host, port):
    sock = socket.create_connection((host, port))
    handle_connection(sock, {
        None: b'\x00\x00\x00\x06\x00\x01\x00\x00\x00\x04',
       b'\x00\x00\x00\x06\x00\x01\x00\x00\x00\x04': b'\x00\x00\x00\x2e\x00\x02\x38\x37\x37\x37\x38\x32\x62\x31\x63\x32\x34\x62\x34\x63\x31\x30\x66\x63\x32\x31\x61\x35\x63\x32\x63\x33\x34\x36\x39\x66\x37\x64\x00\x0a\x50\x6f\x6b\x65\x52\x65\x64\x2e\x67\x62',
       b'\x00\x00\x00\x2e\x00\x02\x38\x37\x37\x37\x38\x32\x62\x31\x63\x32\x34\x62\x34\x63\x31\x30\x66\x63\x32\x31\x61\x35\x63\x32\x63\x33\x34\x36\x39\x66\x37\x64\x00\x0a\x50\x6f\x6b\x65\x52\x65\x64\x2e\x67\x62': b'\x00\x00\x00\x02\x00\x03',
    })

def do_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    (client, address) = sock.accept()
    handle_connection(client, {
       b'\x00\x00\x00\x06\x00\x01\x00\x00\x00\x04': b'\x00\x00\x00\x06\x00\x01\x00\x00\x00\x04',
       b'\x00\x00\x00\x2e\x00\x02\x38\x37\x37\x37\x38\x32\x62\x31\x63\x32\x34\x62\x34\x63\x31\x30\x66\x63\x32\x31\x61\x35\x63\x32\x63\x33\x34\x36\x39\x66\x37\x64\x00\x0a\x50\x6f\x6b\x65\x52\x65\x64\x2e\x67\x62': b'\x00\x00\x00\x2e\x00\x02\x38\x37\x37\x37\x38\x32\x62\x31\x63\x32\x34\x62\x34\x63\x31\x30\x66\x63\x32\x31\x61\x35\x63\x32\x63\x33\x34\x36\x39\x66\x37\x64\x00\x0a\x50\x6f\x6b\x65\x52\x65\x64\x2e\x67\x62',
       b'\x00\x00\x00\x02\x00\x03': b'\x00\x00\x00\x02\x00\x03',
    })


def main():
    parser = argparse.ArgumentParser(description='Pokemon Link')
    parser.add_argument(
        '--host', required=True, help='Host to connect to or bind on'
    )
    parser.add_argument(
        '--port', type=int, required=True, help='Port to connect to or bind on'
    )
    parser.add_argument(
        '--listen', help='Start a server rather than a client', action='store_true'
    )
    args = parser.parse_args()

    if args.listen:
        do_server(args.host, args.port)
    else:
        do_client(args.host, args.port)


if __name__ == '__main__':
    main()
