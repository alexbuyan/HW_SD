
# -- Parser --

# # -- Interpreter --
# def evaluate_arg(arg: str):
#     return arg
#
#
# def evaluate_args(args: Args):
#     transformed_args = []
#     for arg in args.values:
#         transformed_args.append(evaluate(arg))
#     return ' '.join(transformed_args)
#
#
# def evaluate_cmd(cmd: Cmd):
#     name = cmd.name
#     args = cmd.args
#     tranformed_args = evaluate(args)
#     stream = os.popen(f"{name} {tranformed_args}")  # might freeze ????
#     result = stream.read()
#     stream.close()
#     return result
#
#
# def evaluate_pipeline(pipeline: Pipeline):
#     cmd1 = pipeline.cmd1
#     cmd2 = pipeline.cmd2
#     pipe = pipeline.pipe
#     res1 = evaluate(cmd1)
#     if not cmd2:
#         return res1  # if this was not pipeline and just one command
#     res2 = evaluate(cmd2)
#     stream = os.popen(f"{res2} {res1}")  # doesn't work like this ????
#     result = stream.read()
#     stream.close()
#     return result
#
#
# def evaluate(node):
#     if isinstance(node, Cmd):
#         return evaluate_cmd(node)
#     elif isinstance(node, Args):
#         return evaluate_args(node)
#     elif isinstance(node, Pipeline):
#         return evaluate_pipeline(node)
#     return evaluate_arg(node)
#
#
# def interpreter(cli_ast):
#     return evaluate(cli_ast)
#
#
# # -- Interpreter --
#
#
# if __name__ == "__main__":
#     cli_ast = parse("echo 123.txt")
#     result = evaluate(cli_ast)
#     print(result)
