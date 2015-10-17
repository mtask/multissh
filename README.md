#Multissh

If you need to operate with multiple servers through ssh then with Multissh you can run needed commands only once and they will be executed on all your servers.

##Usage

- Configuration

Config your servers to multissh.conf with the following syntax(without ""), one server per line:

"user@server=user"

To use different port jus put port after server, e.g:

 "user@server:1234=user"

Servers can be commented out with "#" in front of the line.

- Run multissh example:

$ python multissh.py -c "echo Hello $(whoami)"

Command with spaces needs to be wrapped inside "".

- Run as sudo:

$ python multissh.py -S "apt-get udate && apt-get upgrade"

- Run local script on server(s):

$ python multissh -s myscript.sh

Script will be copied to server and then it's executed.

###Other info

Multissh's automation works best when authentication is done via ssh keys, but if you practise bad password handeling and have same password for multiple servers then you can run multissh with giving password only one time with [-p/--pass] switch. 

Atm. default path to private key is "~/.ssh/id_rsa" so with different path/key-type it needs to be changed to code. It's coming up feature to set path in config file. If used with password auth and different authentication then ofc. password for every sevrer has to be provided when connection is made.

One version of multissh is also found as a module in my AdminShell repo.
