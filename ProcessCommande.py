# coding=utf-8
import os
import time
import subprocess
import threading

import paramiko

class ProcessCommande:

    def __init__(self, ssh_server = '', ssh_user = '', ssh_password = ''):
        """
        :param ssh_server: ip of the ssh server
        :param ssh_user: user of the ssh server
        :param ssh_password: password of the ssh server
        The constructor of the class ProcessCommande will connect to the ssh server if the ssh_server is not empty
        if the ssh_server is empty, the constructor will execute the commande directly on the local machine
        """
        self.isSSH = ssh_server != ''
        self.ssh_server = ssh_server
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.connect()

    def execute(self, commande, noBlock = False):
        """
        :param commande: commande to execute
        :return: result of the command
        """
        print("-------------------------------------------------")
        print('Execution de la commande "' + commande +'"')
        if self.isSSH:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command(commande)
            result = self.stdout.read().decode('utf-8')
        else:
            if noBlock: # execution non bloquante
                print('Execution non bloquante')
                p = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                time.sleep(1)
                p.terminate()
                result = ''
            else: # execution bloquante
                result = os.popen(commande).read()
        print(result)
        print("-------------------------------------------------")
        return result

    def setDisplay(self):
        if os.environ.get('DISPLAY', '') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')
            self.execute("export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0")
            self.execute('xhost +')

    def connect(self):
        """
        connect to the ssh server using the ssh_user and ssh_password
        """
        if self.isSSH:
            print('Connexion au serveur SSH ' + self.ssh_server)
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ssh_server, username=self.ssh_user, password=self.ssh_password)
            print('Connexion SSH réussie')
            # sudo mode
            print("Passage en mode sudo pour l'execution des commandes")
            self.channel = self.ssh.invoke_shell()
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command("sudo wifite")
            self.stdin.write(self.ssh_password + '\n')
            self.stdin.flush()
            print(self.stdout.read().decode('utf-8'))
        else:
            self.setDisplay()
            print('Pas de connexion SSH')


def sudo_run_commands_remote(command, server_address, server_username, server_pass):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=server_address,
                username=server_username,
                password=server_pass)
    session = ssh.get_transport().open_session()
    session.set_combine_stderr(True)
    session.get_pty()
    session.exec_command("sudo bash -c \"" + command + "\"")
    stdin = session.makefile('wb', -1)
    stdout = session.makefile('rb', -1)
    stdin.write(server_pass + '\n')
    stdin.flush()
    print(stdout.read().decode("utf-8"))

def passSudo(commadeProcessor):
    """
    :param commadeProcessor: instance of the class ProcessCommande
    :return:
    """
    print('Passage en sudo')
    password = commadeProcessor.ssh_password
    commande = 'sudo -S \n ' + 'echo "' + password + '\n'
    commadeProcessor.execute(commande)