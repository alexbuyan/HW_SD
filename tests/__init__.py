import os

from src.parse_manager import ParseManager


class Tester:
    def __init__(self):
        self.parser_manager = ParseManager()

    def __check_result(self, command_str: str, expected_result: str):
        cli_result = self.parser_manager.process_input(command_str)
        assert (cli_result == expected_result)

    def test_echo_eval(self):
        self.__check_result(command_str="echo something",
                            expected_result="something\n")

    def test_cat_eval(self):
        self.__check_result(command_str="cat test_file.txt",
                            expected_result="Some text! Have a nice day!\n")

    def test_wc_eval(self):
        self.__check_result(command_str="wc test_file.txt",
                            expected_result="       1       6      28 test_file.txt\n")

    def test_pwd_eval(self):
        command_str = "pwd"
        expected_result = os.getcwd() + '\n'
        self.__check_result(command_str, expected_result)

    #def test_var_declaration(self):
    #    declaration_result = self.parser_manager.process_input("n=10")
    #    assert(declaration_result == "")
    #    self.__check_result(command_str="echo $n",
    #                        expected_result="10\n")

    def run_tests(self):
        self.test_echo_eval()
        self.test_cat_eval()
        self.test_wc_eval()
        self.test_pwd_eval()
        #self.test_var_declaration()


if __name__ == "__main__":
    tester = Tester()
    tester.run_tests()
