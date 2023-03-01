class InterpreterException(Exception):
    message = "Executing command error"


class UnexpectedTokenException(InterpreterException):
    message = "Unexpected token error"


class UnknownCommand(InterpreterException):
    message = "Unknown command error"


class InvalidArgumentException(InterpreterException):
    message = "Invalid argument error"


class InvalidArgumentNumberException(InterpreterException):
    message = "Invalid number of arguments error"
