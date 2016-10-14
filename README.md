#Multissh

Run same command on multiple servers. SSH key base authentication is needed.

## Configuration

- Servers
Put your servers to multissh.conf with the following syntax(without ""), one server per line:

"user@server=user"

To use different port jus put port after server, e.g:

 "user@server:1234=user"

Servers can be commented out with "#" in front of the line.

- SSH key path

To use different path than  "~/.ssh/id_rsa" set "keypath=path_to_rsa_key" to multissh.config. It doesn't matter if "path=" line is before or after servers.

## Usage

- Run multissh example:

$ python multissh.py -c "echo Hello $(whoami)"

Command with spaces needs to be wrapped inside "".

- Run as sudo:

$ python multissh.py -S "apt-get udate && apt-get upgrade"

- Run local script on server(s):

$ python multissh -s myscript.sh

Script will be copied to server and then executed.
