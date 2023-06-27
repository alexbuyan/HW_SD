import time
import grpc
import entities_pb2 as pb2
import entities_pb2_grpc as pb2_grpc
from datetime import datetime
from concurrent import futures

class ChatServicer(pb2_grpc.ChatServicer):
    def __init__(self):
        self.messages = []
        self.clients = []

    def send(self, request, context):
        message = {'sender_name': request.sender_name, 'message_text': request.message_text, 'timestamp': request.timestamp}
        self.messages.append(message)
        print('[RECEIVED MESSAGE]')
        print(f'\tFrom: {request.sender_name}')
        print(f'\tWhen: {datetime.fromtimestamp(request.timestamp)}')
        print(f'\tMessage: {request.message_text}')
        self.broadcast(request)
        return pb2.Void()

    def receive(self, request, context):
        for message in self.messages:
            yield pb2.Message(sender_name=message['sender_name'], message_text=message['message_text'],
                                       timestamp=message['timestamp'])

    def broadcast(self, request):
        for client in self.clients:
            if client['name'] != request.sender_name:
                response = pb2.Message(sender_name=request.sender_name, message_text=request.message_text,
                                                timestamp=request.timestamp)
                try:
                    client['stub'].send(response)
                except:
                    print(f"Unable to send message to client {client['name']}")

    def register(self, request, context):
        client = {'name': request.name,
                  'stub': pb2_grpc.ChatStub(channel=grpc.insecure_channel(context.peer()))}

        self.clients.append(client)
        print(f"Registered client {request.name}")
        return pb2.Void()

class Server:
    def __init__(self, port=8000):
        self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        pb2_grpc.add_ChatServicer_to_server(ChatServicer(), self.__server)
        self.__server.add_insecure_port(f'[::]:{port}')

    def run(self):
        self.__server.start()
        print('== SERVER STARTED ==')
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            self.__server.stop(0)


if __name__ == "__main__":
    port = input("> Enter server port: ")
    server = Server(port)
    server.run()
