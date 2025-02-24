import socket
import threading

# 서버 설정
HOST = '0.0.0.0' # 모든 네트워크 인터페이스에서 연결 허용
PORT = 5555

# 클라이언트 목록 저장
clients = []

def handle_client(client_socket, address):
    print(f"[연결됨] {address} 가 연결되었습니다.")
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"[{address}] {msg}")
            broadcast(msg, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5) # 최대 5개의 클라이언트 대기
    print(f"[서버 시작] {HOST}:{PORT} 에서 대기 중...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
    