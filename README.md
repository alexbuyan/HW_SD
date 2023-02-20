# Проект по SD (CLI)

## Навигация
* [Диаграмма](https://github.com/alexbuyan/HW_SD/tree/hw1#%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0)
* [Описания классов](https://github.com/alexbuyan/HW_SD/tree/hw1#%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D1%8F-%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%BE%D0%B2)

    * [GUI](https://github.com/alexbuyan/HW_SD/tree/hw1#gui)
    * [ParseManager](https://github.com/alexbuyan/HW_SD/tree/hw1#parsemanager)
    * [Lexer](https://github.com/alexbuyan/HW_SD/tree/hw1#lexer)
    * [Token + TokenType](https://github.com/alexbuyan/HW_SD/tree/hw1#token)
    * [Parser](https://github.com/alexbuyan/HW_SD/tree/hw1#parser)
    * [Command](https://github.com/alexbuyan/HW_SD/tree/hw1#command)
    * [*Exception](https://github.com/alexbuyan/HW_SD/tree/hw1#exception)


## Диаграмма
<img src="/images/CLI_diagram.png"/>

## Описания классов
### GUI
Этот класс реализует графический интерфейс командной строки
###### Cтруктура класса
```
GUI {
	parseManager: ParseManager() // логика работы CLI

	// метод в бесконечном режиме получает введенные
	// пользователем команды и передает их ParseManager
	// для разбора.
	void run() // запускает GUI

	void exit() // останавливает GUI
}
```

### ParseManager
Этот класс собирает в себе всю основную логику нашего приложения. Мы будем использовать следующую логику:
* Передаем ввод пользователя в Lexer
* Получаем из него список токенов (Token), который передаем в Parser
* По ним Parser проводит синтаксический анализ и строит дерево разбора (AST)
* AST передаем на вход Interpreter, который разбирается, как правильно выполнить команды
###### Cтруктура класса
```
ParseManager {
	lexer: Lexer()
	parser: Parser()
	interpreter: Interpreter()

	// прогоняет строчку, полученную из GUI, через наш алгоритм,
	// который выполнит команду
	void executeCommand(String command)
}
```

### Lexer
Этот класс отвечает за лексический анализ и по входной последовательности получает список токенов
###### Cтруктура класса
```
Lexer {
	// метод, который проводит лексический анализ
	List<Token> lex(String input)
}
```

### Token
У нас будет описание нашей грамматики через различные типы токенов (TokenType):
```
// Примерное описание грамматики
TokenType : Arg
          | Args
          | Command
          | CommandName

Command : CommandName + ' ' + Args

CommandName : String

Args : Arg
     | Arg + ' ' + Args

Arg : String
```
Token - это примитивная структура, которая будет хранить тип токена из нашей грамматики и его значение.

По этим токенам парсер будет строить дерево разбора
###### Cтруктура
```
Token {
    tokenType: TokenType
    tokenValue: String
}
```

### Parser
Этот класс занимается синтаксическим анализом и собственно строит дерево разбора
###### Cтруктура класса
```
Parser {
	// запоминает токены, полученные из лексера, 
	// для дальнейшей работы парсера
	void init(List<Token> tokens)

	// метод выполняет парсинг и возвращает полученное AST
	AST parse()
}
```

### Interpreter
Парсер из введенной пользователем команды построил AST. По этому AST класс Interpreter выполняет саму команду 
###### Cтруктура класса
```
Interpreter {
	void executeCommand(AST ast)
}
```

### Command
Чтобы выполнять команды, интерпретатор должен знать логику их работы. Command - абстрактный класс, от которого наследуются реализации для наших конкретных комманд
###### Cтруктура класса
```
Command {
	name: String
	args: List<String>

	void execute()
	// наследники переопределяют этот метод и 
	// задают конкретную логику
}
```
###### Наследники Command
* CatCommand
* EchoCommand
* WcCommand
* PwdCommand
* ExitCommand

### *Exception
Классы для обработки специализированных исключений

###### Виды исключений
- UnexpectedTokenException - встретился токен, который парсер не ожидал
- UnknownCommand - неизвестная команда
- InvalidArgument - команде был передан неожиданный аргумент
- InvalidNumberOfArguments - команде было передано неправильное количество аргументов