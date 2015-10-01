#!/usr/bin/python

from fabric.api import *
from fabric.tasks import execute
import sys, os, argparse, getpass

"""
Author: mtask@github.com
"""


class multissh(object):

    def get_hosts(self):
        self.hosts = []
        self.users = []
        with open('multissh.conf','r') as conf:
            for self.host in conf:
                if self.host.startswith("#"):
                    continue
                self.params = self.host.split('=',1)
                print self.params
                self.hosts.append(self.params[0])
                self.users.append(self.params[1])
        
        return (self.hosts, self.users)
        
    def run_script(self,script,sudo_=False, passw=False):
	       '''Copy local script to host and execute it'''
	       put(script, script, mode=0755)
	       if sudo_:
	           sudo("./"+script)
	       else:
	           run("./"+script)
        
            
    def run_cmd(self, cmd,sudo_=False, script=False, passw=False):
    
        self.failed = []
        self.cmd = cmd
        self.servers,self.users = self.get_hosts()
        os.path.expanduser("~/")
        for self.s, self.u in zip(self.servers, self.users):
            if os.path.isfile("~/.ssh/id_rsa") and passw == False:
                with settings(host_string=self.s, user=self.u, key_filename="~/.ssh/id_rsa"):
                    try:
                        if script:
                            if sudo_:
                                self.run_script(self.cmd, sudo_=True)
                            else:
                                self.run_script(self.cmd)
                        else:
                            if sudo_:
                                sudo(self.cmd)
                            else:
                                run(self.cmd)

                       
                    except Exception as e:
                        self.failed.append(self.t)
                        print "Execution failed on: "+self.t
                        print "Error:"+str(e)
            elif passw:
                with settings(host_string=self.s, user=self.u, password=passw):
                    try:
                        if script:
                            if sudo_:
                                self.run_script(self.cmd, sudo_=True)
                            else:
                                self.run_script(self.cmd)
                        else:
                            if sudo_:
                                sudo(self.cmd)
                            else:
                                run(self.cmd)
                       
                    except Exception as e:
                        self.failed.append(self.s)
                        print "Execution failed on: "+self.s
                        print "Error:"+str(e)

                
                        
            else:
                with settings(host_string=self.s, user=self.u):
                    try:
                        if script:
                            if sudo_:
                                self.run_script(self.cmd, sudo_=True)
                            else:
                                self.run_script(self.cmd)
                        else:
                            if sudo_:
                                sudo(self.cmd)
                            else:
                                run(self.cmd)
                       
                    except Exception as e:
                        self.failed.append(self.s)
                        print "Execution failed on: "+self.s
                        print "Error:"+str(e)

        if len(self.failed) == 0:
            print "Command executed on all servers"
        else:
            print "[!] Execution failed on:"
            for f in self.failed:
                print f
                
    def parse_args(self):
        self.descr = """
            Easily run commands through multiple ssh servers.
            Configurate hosts to multissh.conf
            """
        self.parser = argparse.ArgumentParser(description=self.descr)
        self.parser.add_argument("-c", "--cmd", type=str, help="Run command script on servers. Wrap commans inside \"\"")
        self.parser.add_argument("-s", "--script", type=str, help="Run local script on servers")
        self.parser.add_argument("-S", "--sudo", action='store_true', help="Run with sudo")
        self.parser.add_argument("-p", "--passw", action='store_true', help="Set password if same in all logins")
        
        self.args = self.parser.parse_args()
        return self.args
        
    def main(self):
        self.arg = self.parse_args()
        self.passw_ = False
        if self.arg.passw:
            self.passw_ = getpass.getpass("Give password> ")
        if self.arg.cmd:
             if self.arg.sudo:
                 self.run_cmd(self.arg.cmd, sudo_=True,passw= self.passw_)
             else:
                 self.run_cmd(self.arg.cmd, passw=self.passw_)
        if self.arg.script:
            if self.arg.sudo:
                self.run_cmd(self.arg.script, sudo_=True, script=True, passw=self.passw_)
            else:
                self.run_cmd(self.arg.script, script=True,passw=self.passw_)  

                                     
if __name__=='__main__':
    multissh().main()
    