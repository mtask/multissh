#!/usr/bin/python

from fabric.api import *
from fabric.tasks import execute
import sys, os, argparse, getpass
import ntpath

"""
Author: mtask@github.com
"""


class multissh(object):

    def get_settings(self, list=False):
        self.hosts = []
        self.users = []
        self.keypath = None
        with open('multissh.conf','r') as conf:
            for self.config in conf:
                if self.config.startswith("#"):
                    continue
                elif self.config.startswith("keypath="):
                    try:
                        self.keypath = self.config.split('=',1)[1].strip()
                    except Exception as e:
                        raise e
                else:
                    try:
                        self.params = self.config.split('=',1)
                        self.hosts.append(self.params[0])
                        self.users.append(self.params[1])
                    except Exception as e:
                        raise e
        if list:
            self.server_num = 1
            for self.h in self.hosts:
                print "["+str(self.server_num)+"] "+self.h
                self.server_num += 1
        else:
            return (self.hosts, self.users, self.keypath)


    def run_cmd(self, cmd,sudo_=False, script=False):
        self.failed = []
        self.cmd = cmd
        self.servers,self.users, self.keypath = self.get_settings()
        os.path.expanduser("~/")

        if not self.keypath:
            if os.path.isfile(os.path.expanduser("~/")+".ssh/id_rsa"):
                self.keypath = "~/.ssh/id_rsa"
            else:
                print "[!] No clue where the ssh keys are..."
                sys.exit(0)

        for self.s, self.u in zip(self.servers, self.users):
            with settings(host_string=self.s, user=self.u, key_filename=self.keypath):
                try:
                    if script:
                        if os.path.isfile(self.cmd):
                            put(self.cmd, "tempscript", mode=0755)
                        else:
                            print "[!] Path to local script not found."
                            sys.exit(1)
                        if sudo_:
                            sudo("./tempscript")
                            sudo("rm tempscript")
                        else:
                            run("./tempscript")
                            run("rm tempscript")
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
            if script:
                print "Script executed on all servers"
            else:
                print "Command executed on all servers"
        else:
            print "[!] Execution failed on:"
            for f in self.failed:
                print f

    def parse_args(self):
        self.descr = """
            Easily run commands through multiple ssh servers.
            Configurate hosts to multissh.conf.
            Example configuration: user@server=user
            """
        self.parser = argparse.ArgumentParser(description=self.descr)
        self.parser.add_argument("-c", "--cmd", type=str, help="Run command script on servers. Wrap commans inside \"\"")
        self.parser.add_argument("-s", "--script", type=str, help="Path to local script to move and run on servers")
        self.parser.add_argument("-S", "--sudo", action='store_true', help="Run with sudo")
        self.parser.add_argument("-l", "--list", action='store_true', help="List servers")
        self.args = self.parser.parse_args()
        return self.args

    def main(self):
        self.arg = self.parse_args()
        if self.arg.list:
            self.get_settings(list=True)
            sys.exit(0)
        if self.arg.cmd:
             if self.arg.sudo:
                 self.run_cmd(self.arg.cmd, sudo_=True)
             else:
                 self.run_cmd(self.arg.cmd)
        if self.arg.script:
            if self.arg.sudo:
                self.run_cmd(self.arg.script, sudo_=True, script=True)
            else:
                self.run_cmd(self.arg.script, script=True)


if __name__=='__main__':
    multissh().main()
