class InterpreterEvaluationException(Exception):
    def __init__(self, message: str = "Error while interpreter command evaluation"):
        self.__message = message

    def get_message(self):
        return self.__message
