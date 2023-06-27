import grpc
import entities_pb2 as pb2
import entities_pb2_grpc as pb2_grpc
from datetime import datetime
import time

class Client:
    def __init__(self, host='localhost', port=8000):
        self.__host = host
        self.__port = port
        self.__channel = grpc.insecure_channel('{}:{}'.format(self.__host, self.__port))
        self.__stub = pb2_grpc.ChatStub(channel=self.__channel)
        self.__username = None

    def register(self, username):
        if self.__username:
            return
        self.__username = username
        self.__stub.register(pb2.Client(name=self.__username))

    def run(self):
        try:
            while True:
                message_text = input("> Enter a message: ")
                if message_text.lower() == "exit":
                    break
                self.__stub.send(pb2.Message(sender_name=self.__username, message_text=message_text, timestamp=int(time.time())))
                responses = self.__stub.receive(pb2.Void())
                for response in responses:
                    print('[MESSAGE]')
                    print(f'\tFrom: {response.sender_name}')
                    print(f'\tWhen: {datetime.fromtimestamp(response.timestamp)}')
                    print(f'\tMessage: {response.message_text}')
        except KeyboardInterrupt:
            pass
        

if __name__ == "__main__":
    host = input("> Enter peer (default=localhost): ") or 'localhost'
    port = input("> Enter port (default=8000): ") or 8000
    client = Client(host, port)
    username = input("> Enter username: ")
    client.register(username)
    client.run()