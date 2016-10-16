#Multissh

Run command, script or copy files on multiple servers at same time.

## Configuration

- Servers

Add your ssh public key to server.

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

- Run local script on serves:

$ python multissh -s myscript.sh

- Copy file from local machine to servers:

$ python multissh -cf /path/to/myfile.file


Script will be copied to server and then executed.

- Other options

   - -yn/--yesno -> Check on every server if to run command on that server.

   - -l/--list -> List servers from config: python multissh.py -l

   - -a/--add -> Add server to multissh.conf: python multissh.py -a "user@newserver:2222=user"

   - -d/--delete -> Delete server from multissh.conf. Use list command to get server's number: python multissh.py -d number
