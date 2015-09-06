
import argparse
import socket
import fabric
from fabric.api import env, run, settings

## Help by https://gist.github.com/redja/9276216
## http://code.activestate.com/recipes/577769-tcp-port-checker/


''' Building the dictionary of services and mapping the ports to it '''
services = {
	'22' : 'sshd',
	'80' : 'httpd',
	'3306' : 'mysql'
}

def get_args():
    '''This function parses and return arguments passed in'''
    # Assign description to the help doc
    parser = argparse.ArgumentParser(
        description='Script checks open TCP ports for a given server')
    # Add arguments
    parser.add_argument(
        '-H', '--host', type=str, help='Host IP', required=True)
    parser.add_argument(
        '-p', '--port', type=str, help='Port number', required=True, nargs='+')
    
    # Array for all arguments passed to script
    args = parser.parse_args()
    # Assign args to variables
    server = args.host
    port = args.port[0].split(",")
    # Return all variable values
    return server, port


''' Checking the ports of a given IP and ports passed'''
def check_server(address, port):
	# Create a TCP socket
	s = socket.socket()
	s.settimeout(0.3)
	# print "Attempting to connect to %s on port %s" % (address, port)
	try:
		s.connect((address, port))
		#print "Connected to %s on port %s" % (address, port)
		return True
	except socket.error, e:
		#print "Connection to %s on port %s failed: %s" % (address, port, e)
		return False


server, port = get_args()
env.hosts = [server]
env.user = "apple"
env.password = "Fatoom@2015"



# Print the values
print "\nHost IP: [ %s ]\n" % server

for p in port:
    if (check_server(server, int(p))):
    	print '\360\237\215\272  Port %s is open and running \n\n' % p
    
    else:
    	print 'Port %s is closed or not running' % p
    	with settings(host_string=server):
    		try:
    			run('service start %s' % services[p])
    		except: 
				pass
