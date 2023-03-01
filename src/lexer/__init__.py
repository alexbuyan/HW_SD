grammar = """
%import common.NUMBER
%import common.WS
%ignore WS

start: pipeline
     | envs_init
     | env

pipeline: (cmd pipe)* cmd
pipe: /\|/

cmd: cmd_name args
cmd_name: "cat" | "echo" | "wc" | "pwd" | "exit"

args: arg*
arg: "$" env_name
   | /\"$env_name\"/
   | /([^\s"\'\|]+)/
   | /\'([^\']*)\'/
   | /"([^"]*)"/
   
env: "$" env_name
   
envs_init: env_init*
env_init: env_name "=" arg
        
env_name: /([A-Za-z][\_A-Za-z0-9]*)/
"""
