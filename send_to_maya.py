import socket

def send_to_maya(script_path):
    host = '127.0.0.1'
    maya_port = 4434
    with open(script_path, 'r') as file:
        script_content = file.read()

    # Échapper correctement les guillemets pour l'utilisation dans MEL
    script_content = script_content.replace('"', '\\"').replace('\n', '\\n')
    mel_command = f'python("{script_content}")'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, maya_port))
        s.send(f'{mel_command}\n'.encode('utf-8'))
        s.close()
        print("Script sent successfully.")
    except ConnectionRefusedError:
        print("Connection refused. Make sure Maya is running and commandPort is open.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    send_to_maya('main.py')
