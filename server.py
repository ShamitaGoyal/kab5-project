import os
import socket

HOST = 'localhost'  # Server hostname
PORT = 5551


def change_directory(new_directory):
    """
    Change directory; return "success" or "fail".
    """
    try:
        os.chdir(new_directory)
        return "success"
    except FileNotFoundError:
        return "fail - No such directory"
    except OSError as e:
        return f"fail - {str(e)}"


def list_current_d():
    """
    List the directories and files in the current directory.
    """
    try:
        files = os.listdir(".")
        return "\n".join(files)
    except Exception as e:
        return str(e)


def recursive_d():
    """
    Send the list of subdirectories from a recursive
    walk of the client's current directory.
    """
    sub_d = []
    for root, dirs, _ in os.walk("."):
        for d in dirs:
            sub_d.append(os.path.join(root, d))
    return "\n".join(sub_d)


def handle_client(conn):
    """
    Handle client requests.
    """
    commands_dict = {
        "cd": lambda args: change_directory(args[0]) if len(args) == 1 else "Invalid cd command",
        "ls": lambda _: list_current_d(),
        "lsr": lambda _: recursive_d()
    }

    while True:
        request = conn.recv(1024).decode().strip()
        if not request:
            break

        command_parts = request.split()
        command = command_parts[0]
        args = command_parts[1:]

        if command == "q":
            break

        if command in commands_dict:
            response = commands_dict[command](args)
            conn.sendall(response.encode())

    conn.close()


def main():
    """
    Main server function.
    """
    with socket.socket() as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server is up, hostname: {HOST}, port: {PORT}')
        print(f"Starting directory: {os.getcwd()}")


        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            handle_client(conn)


if __name__ == "__main__":
    main()
