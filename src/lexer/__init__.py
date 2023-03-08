grammar = """
%import common.WS
%import common.EQUAL
%ignore WS

start: pipeline
     | env_init
     | env_call

pipeline: (cmd pipe)* cmd
pipe: /\|/

cmd: cmd_name args
!cmd_name: "cat"|"echo"|"wc"|"pwd"|"exit"

args: val*
env_init: env_name "=" val

val: "$"env_name
   | /\"$env_name\"/
   | /([^\s"\'\|]+)/
   | /\'([^\']*)\'/
   | /"([^"]*)"/
   
env_call: "$"env_name    
env_name: /([A-Za-z][\_A-Za-z0-9]*)/
"""
