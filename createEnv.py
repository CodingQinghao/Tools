import os
import random
from notebook.auth import passwd

def getRandomSet(bits):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set

    value_set = "".join(random.sample(total_set, bits))

    return value_set

password = getRandomSet(6)
random_title = random.randint(100000, 199999)
ssh_port = random.randint(10000, 19999)
jupyter_port = random.randint(20000, 29999)

#start open ssh-server
os.system('apt update')
os.system('apt install openssh-server -y')
os.system('echo "root:'+str(password)+'" | sudo chpasswd')
os.system('echo "Port 22" >> /etc/ssh/sshd_config')
os.system('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
os.system('service ssh start')

#start install frpc
os.system('wget https://github.com/fatedier/frp/releases/download/v0.38.0/frp_0.38.0_linux_386.tar.gz')
os.system('tar -zxvf frp_0.38.0_linux_386.tar.gz')
os.system('chmod +x ./frp_0.38.0_linux_386/frpc')

#start install jupyter
os.system('jupyter notebook --generate-config -y')
os.system('echo \'c.NotebookApp.notebook_dir = "/dev/shm/"\' >> /root/.jupyter/jupyter_notebook_config.py')
passwd(password)
os.system('nohup jupyter notebook &')

#config frpc

f = open('./frp_0.38.0_linux_386/ailab-frpc.ini', 'w')
f.write('[common]\n')
f.write('server_addr = ailab.work\n')
f.write('server_port = 443\n')
f.write('\n')

f.write('[tcp.'+str(random_title)+'.ssh]\n')
f.write('type = tcp\n')
f.write('local_ip = 127.0.0.1\n')
f.write('local_port = 22\n')
f.write('remote_port = '+str(ssh_port)+'\n')
f.write('\n')

f.write('[http.'+str(random_title)+'.ailab.work]\n')
f.write('type = tcp\n')
f.write('local_ip = 127.0.0.1\n')
f.write('local_port = 8888\n')
f.write('remote_port = '+str(jupyter_port)+'\n')
f.write('\n')

os.system('nohup frp_0.38.0_linux_386/frpc -c ./frp_0.38.0_linux_386/ailab-frpc.ini &')

print("\n\n\n\n\n\n")
print("========Configuration succeeded========")
print("ssh:ailab.work:"+str(ssh_port))
print("ssh password:"+str(password))

print("jupyter:http://ailab.work:"+str(jupyter_port))
print("jupyter password:"+str(password))
print("========Configuration succeeded========")
print("\n\n\n\n\n\n")