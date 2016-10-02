import os
cmds = [
    'pip install -r requirements.txt',
    'pyflakes .',
    'pylint models'
]

for cmd in cmds:
    print '\n----> ', cmd
    os.system(cmd)
