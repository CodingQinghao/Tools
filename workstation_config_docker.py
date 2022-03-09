import os
import random
from notebook.auth import passwd

def getRandomSet(bits):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set

    value_set = "".join(random.sample(total_set, bits))

    return value_set


password = input("Please input a password OR automatic generation:")

if password == "":
    password = getRandomSet(6)

ssh_port = input("Please input a SSH port :")
if ssh_port == "":
    ssh_port = 22
jupyter_port = input("Please input a jupyter port:")
if jupyter_port == "":
    jupyter_port = 8000

#start open ssh-server
os.system('apt update')
os.system('apt install openssh-server -y')
os.system('echo "root:'+str(password)+'" | chpasswd')
os.system('echo "Port '+str(ssh_port)+'" >> /etc/ssh/sshd_config')
os.system('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
os.system('service ssh start')


#start install jupyter
os.system('jupyter notebook --generate-config -y')
jupyter_password_sha1 = passwd(str(password))
os.system('echo \'c.NotebookApp.password = "'+str(jupyter_password_sha1)+'" \' >> /root/.jupyter/jupyter_notebook_config.py')
os.system('echo "c.NotebookApp.port = '+str(jupyter_port)+'" >> /root/.jupyter/jupyter_notebook_config.py')
os.system('echo "c.NotebookApp.ip = \'0.0.0.0\'" >> /root/.jupyter/jupyter_notebook_config.py')
os.system('echo "c.NotebookApp.notebook_dir = \'/workspace\'" >> /root/.jupyter/jupyter_notebook_config.py')
os.system('nohup jupyter notebook --allow-root &')


print("\n\n\n\n\n\n")
print("========Configuration succeeded========")
print("ssh:ailab.work")
print("ssh:port:"+str(ssh_port))
print("ssh password:"+str(password))

print("jupyter:http://xx-workstation.procoding.cn:"+str(jupyter_port)+"/")
print("jupyter password:"+str(password))
print("========Configuration succeeded========")
print("\n\n\n\n\n\n")
