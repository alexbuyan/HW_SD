class InterpreterException(Exception):
    def __init__(self, message: str = "Executing command error"):
        self.__message = message


class UnexpectedTokenException(InterpreterException):
    def __init__(self):
        super().__init__("Unexpected token error")


class UnknownCommand(InterpreterException):
    def __init__(self):
        super().__init__("Unknown command error")


class InvalidArgumentException(InterpreterException):
    def __init__(self):
        super().__init__("Invalid argument error")


class InvalidArgumentNumberException(InterpreterException):
    def __init__(self):
        super().__init__("Invalid number of arguments error")
