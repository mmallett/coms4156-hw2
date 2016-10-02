import subprocess
import time
import requests

server = subprocess.Popen(['python', 'server.py'])

print('waiting for server to start')
time.sleep(5)
print('\nrunning tests\n')

print('GET /')
r = requests.get('http://localhost:8111/', )
print r.status_code, '\n'

print('POST /')
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
body = 'message=hello'
r = requests.post('http://localhost:8111/', data=body, headers=headers)
print r.status_code, '\n'

time.sleep(1)
print('stopping server')
server.kill()
server.wait()
