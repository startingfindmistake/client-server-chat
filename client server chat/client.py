import socket
import threading

HOST ='127.0.0.1' # 로컬에서 실행할 경우
PORT = 5555

def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
        except:
            print("[연결 종료] 서버 연결이 끊어졌습니다.")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[서버 연결됨] 메시지를 입력하세요!")

     # 수신 메시지를 별도 스레드로 실행
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        client.send(msg.encode('utf-8'))

    client.close()
    print("[연결 종료] 채팅을 종료합니다.")

if __name__ == "__main__":
    start_client()
