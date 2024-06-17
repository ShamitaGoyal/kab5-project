import socket

HOST = 'localhost'  # Server hostname
PORT = 5551

def handle_choice():
    print("=" * 50)
    print("\nCommands:")
    menu = "\n".join(f"{command:<15} {description}" for command, description in [
        ("ls", "list current directory"),
        ("lsr", "list subdirectories recursively"),
        ("cd dir_name", "go to dir_name"),
        ("q", "quit")
    ])

    print(menu, "\n")
    print("=" * 50)

    while True:
        choice = input('Enter choice: ').strip()
        print("=" * 50)
        if choice in ['ls', 'lsr', 'q'] or (choice.startswith('cd') and len(choice.split()) == 2):
            return choice
        else:
            print('Invalid choice. Try again.')

def send_req_to_server(choice):
    with socket.socket() as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(choice.encode())
            response = s.recv(1024).decode()
        except ConnectionError as e:
            print(f"Error connecting to server: {e}")
            return None

    return response

def process_response(choice, response):
    if choice.startswith("cd"):
        if response == "success":
            print(f"Changed to new directory: {choice.split()[1]}")
        else:
            print("No such directory")

    elif choice in ["ls", "lsr"]:
        print(f"Response from server for {choice}:")
        print(response)

    elif choice == "q":
        print("Quitting client")

def main():
    print("=" * 50)
    print(f"Client connect to: {HOST}, port: {PORT}")
    while True:
        command = handle_choice()
        if command == "q":
            send_req_to_server(command)
            process_response(command, "")
            break
        response = send_req_to_server(command)
        if response is not None:
            process_response(command, response)

if __name__ == "__main__":
    main()
