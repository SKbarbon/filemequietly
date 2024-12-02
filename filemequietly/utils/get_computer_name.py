import socket


def get_computer_name () -> str:
    return str(socket.gethostname())