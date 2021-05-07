import argparse
import socket
import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


class UdpServerAndClient:

    def __init__(self, args):
        self.user = args.user_name
        self.target_ip = args.target_ip
        self.target_port = args.target_port
        self.local_port = args.local_port

        self.away = (str(self.target_ip), int(self.target_port))
        self.home = ('0.0.0.0', int(self.local_port))

        sock.bind(self.home)

    def ping(self):
        ping_message_string = f'0 {self.user} {self.target_ip} {self.target_port}'
        ping_message = ping_message_string.encode()

        while True:
            time.sleep(.5)
            sock.sendto(ping_message, self.away)

    def receive_and_interpret(self):
        while True:
            data, port = sock.recvfrom(55000)
            if data[:1] == b'0':
                pass
            else:
                print(data.decode('utf-8'))

    def send_message(self):
        while True:
            user_input = input()
            package = f'{self.user} - {user_input}'
            if user_input:
                message = package.encode()
                sock.sendto(message, self.away)

    def run(self):
        t1 = threading.Thread(target=self.ping)
        t2 = threading.Thread(target=self.receive_and_interpret)
        t3 = threading.Thread(target=self.send_message)
        t1.start()
        t2.start()
        t3.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_name', help="local user name", nargs='?')
    parser.add_argument('--target_ip', help="ip address for remote peer", nargs='?')
    parser.add_argument('--target_port', help="target port for remote peer", nargs='?')
    parser.add_argument('--local_port', help="local port for udp server / client", nargs='?')
    args = parser.parse_args()
    UdpServerAndClient(args).run()
