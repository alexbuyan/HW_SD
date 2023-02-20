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
Класс, реализующий графический интерфейс командной строки.
###### Cтруктура класса
```
GUI {
	parseManager: ParseManager() // логика работы CLI

	// Запуск GUI. Метод в бесконечном режиме получает введенные пользователем команды и передает их в ParseManager для дальнейшего разбора.
	void run()

	// Остановка GUI.
	void exit()
}
```

### ParseManager
Класс, реализующий обработку переденной ему строки пользователя.
Обработка происходит в несколько этапов:
* Пользовательский ввод поступает на вход Lexer'у. Lexer по строке формирует соответствующий ей список токенов.
* Список токенов, построенный Lexer'ом, поступает на вход Parser'у. Parser проводит синтаксический анализ и строит дерево разбора -- AST.
* Полученное AST передается на вход Interpreter'у, который в нужной последовательности обрабатывает команды, вычлененные из введенной пользователем строки.
###### Cтруктура класса ParseManager
```
ParseManager {
	lexer: Lexer()
	parser: Parser()
	interpreter: Interpreter()

	// Прогоняет строчку, полученную из GUI, через наш алгоритм, который выполнит команду
	void processString(String inputString)
}
```

### Lexer
Класс, производящий лексический анализ. По введенной строке формирует соответствующий набор токенов.
###### Cтруктура класса
```
Lexer {
	// Метод, производящий лексический анализ строки и возвращающий сформированный список токенов
	List<Token> lex(String inputString)
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
Token хранит тип токена из нашей грамматики и его текстовое значение.

По токенам парсер вдальнейшем будет строить дерево разбора.
###### Cтруктура Token
```
Token {
    type: TokenType
    text: String
}
```

### Parser
Класс, производящий синтаксический анализ и строящий дерево разбора AST.
###### Cтруктура класса Parser
```
Parser {
	List<Token> tokens

	// Запоминает токены, полученные из лексера, для дальнейшей работы парсера
	void init(List<Token> tokens)

	// Метод, осуществляющий парсинг списка токенов и возвращающий построенное AST
	AST parse()
}
```

### Interpreter
По этому AST, полученному из Parser'a, Interpreter в нужной последовательности осуществляет вызов команд, введенных пользователем в строке.
###### Cтруктура класса Interpreter
```
Interpreter {
	void executeCommands(AST ast)
}
```

### Command
Чтобы запустить команды на исполнениие, интерпретатор должен знать логику их работы. Command - абстрактный класс, от которого наследуются реализации конкретных комманд.
###### Cтруктура класса Command
```
Command {
	name: String
	args: List<String>

	// Наследники переопределяют этот метод и задают конкретную логику исполнения команды
	void execute()
}
```
###### Классы-наследники Command
* CatCommand
* EchoCommand
* WcCommand
* PwdCommand
* ExitCommand

### Exception
Классы для обработки специализированных исключений.

###### Виды исключений
- UnexpectedTokenException - токен, не включенный в список ожидаемых токенов и не поддерживаемый парсером
- UnknownCommand - неизвестная команда
- InvalidArgument - команде был передан невалидный аргумент
- InvalidNumberOfArguments - команде было передано неверное число аргументов