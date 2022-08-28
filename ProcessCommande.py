# coding=utf-8
import _thread
import os
import signal
import time
import subprocess
from threading import Thread

import paramiko

AUTO_KILL_DELAY = 1  # delay in minutes to kill a process

class ProcessCommande:

    def __init__(self, sudoPassword = 'kali', ssh_server = '', ssh_user = '', ssh_password = ''):
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
        self.sudoPassword = sudoPassword
        self.process = None
        self.connect()

    def execute(self, commande, noBlock = False, root = False, autoKill = False):
        """
        :param commande: commande to execute
        :param noBlock: if True, the commande will be executed in background
        :param root: if True, the commande will be executed as root
        :param autoKill: if True, the process will end after a delay by sending a SIGINT signal
        :return: result of the command
        """
        print("-------------------------------------------------")
        print('Execution de la commande "' + commande +'"')
        result = '' # initialize the result
        try:
            if self.isSSH:
                self.stdin, self.stdout, self.stderr = self.ssh.exec_command(commande)
                result = self.stdout.read().decode('utf-8')
            else:
                if root:
                    commande = 'echo %s|sudo -S %s' % (self.sudoPassword, commande)
                if noBlock: # execution non bloquante
                    print('Execution non bloquante')
                    p = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    time.sleep(2)
                    p.terminate()
                elif autoKill:
                    self.process = subprocess.Popen(commande, stdout=subprocess.PIPE, shell=True)
                    while self.process.poll() is None:
                        time.sleep(AUTO_KILL_DELAY)
                        result = self.process.communicate()[0].decode('utf-8')  # get the result of the command
                        self.process.terminate()
                        return result
                else: # execution bloquante
                    self.process = subprocess.Popen(commande, stdout=subprocess.PIPE, shell=True)
                    self.process.wait() # wait for the end of the command
                    result = self.process.communicate()[0].decode('utf-8') # get the result of the command
                    self.process = None # no process in runing
        except Exception as e:
            print(e)
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
            #self.setDisplay()
            print('Pas de connexion SSH')

    def sigint(self):
        """
        kill the process if the user press Ctrl+C
        return True if the process is killed
        """
        print("\n")
        # Get the process id
        if self.process is not None:
            pid = self.process.pid
            os.kill(pid, signal.SIGINT)
            if not self.process.poll():
                print("Process correctly halted pid : " + str(pid))
            return True
        else:
            print("Pas de process à arrêter")
        return False

    def autoKill(self, pid, commande, process):
        """
        kill the process after a delay by sending a SIGINT signal
        """
        print("Auto kill in " + str(AUTO_KILL_DELAY) + " minutes")
        delay = 60 * AUTO_KILL_DELAY
        time.sleep(delay)
        #check if the process is still running
        while check_pid(pid):
            _thread.interrupt_main()
            process.send_signal(signal.SIGINT)
            print("\nAUTO KILL pid: " + str(pid) + " commande : " + commande)
            os.kill(pid, signal.CTRL_C_EVENT)
            self.autoKill(pid, commande, process)



def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True



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
    print("-------------------------------------------------")
    print('Passage en sudo')
    password = input('Entrez le mot de passe de l\'utilisateur root : ')
    commande = 'sudo -S \n ' + 'echo "' + password + '"\n'
    commadeProcessor.execute(commande)