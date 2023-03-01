import os

from src.parse_manager import ParseManager


class Tester:
    def __init__(self):
        self.parser_manager = ParseManager()

    def __check_result(self, command_str: str, expected_result: str):
        cli_result = self.parser_manager.process_input(command_str)
        print("cli_result: {}".format(cli_result))
        assert (cli_result == expected_result)

    def test_echo_eval(self):
        self.__check_result(command_str="echo something",
                            expected_result="something\n")

    def test_echo_single_quotes(self):
        self.__check_result(command_str="echo 'something in single quotes'",
                            expected_result="something in single quotes\n")

    def test_echo_double_quotes(self):
        self.__check_result(command_str='echo "something in double quotes"',
                            expected_result="something in double quotes\n")

    def test_cat_eval(self):
        print(os.getcwd())
        self.__check_result(command_str="cat tests/test_file.txt",
                            expected_result="Some text! Have a nice day!\n")

    def test_wc_eval(self):
        command_str = "wc tests/test_file.txt"
        self.__check_result(command_str=command_str,
                            expected_result=os.popen(command_str).read())

    def test_pwd_eval(self):
        command_str = "pwd"
        expected_result = os.getcwd() + '\n'
        self.__check_result(command_str, expected_result)

    def test_var_declaration_and_dollar(self):
        self.parser_manager.process_input("n = 10")
        self.__check_result(command_str="echo $n",
                            expected_result="10\n")

    def run_tests(self):
        self.test_echo_eval()
        self.test_echo_single_quotes()
        self.test_echo_double_quotes()
        self.test_cat_eval()
        self.test_wc_eval()
        self.test_pwd_eval()
        self.test_var_declaration_and_dollar()
