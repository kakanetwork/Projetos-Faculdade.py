import os, subprocess

dir_atual = os.path.dirname(os.path.abspath(__file__))  # pegando a pasta atual
dir_arq =  os.path.abspath(__file__)
dir_temp = dir_atual + "\\Server-Principal"

pid = 58552
proc = subprocess.check_output(['tasklist', '/NH', '/FI', f'PID eq {pid}'])
print(proc)