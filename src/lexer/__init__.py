grammar = """
%import common.NUMBER
%import common.WS
%ignore WS

start: pipeline
     | statement
     | vars
            
vars: var*
var: /\$[\w.\w]+/
        
statement: name "=" value

name: /\w/+
        
value: /\S+.\w+/
     | /\S+/
     | NUMBER

pipeline: (cmd pipe)* cmd
pipe: /\|/

cmd: cmd_name args
cmd_name: /(cat|echo|wc|pwd|exit)/

args: arg*
arg: /\S+.\w+/
   | /\S+/
"""
