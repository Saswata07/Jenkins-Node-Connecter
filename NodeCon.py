import subprocess
import sys
import xml.etree.ElementTree as ET 
import requests

jenkins_url = sys.argv[1]
nodepath = sys.argv[2]
jenkins_user = sys.argv[3]
jenkins_pass = sys.argv[4]
temp_path = "c:/Temp/"
nodes = nodepath.split(",")
print(jenkins_url)
print(nodepath)
auth = (jenkins_user, jenkins_pass)
r = requests.get(jenkins_url + "jnlpJars/agent.jar", allow_redirects=True, auth=auth)
open(temp_path + 'agent.jar', 'wb').write(r.content)
for node in nodes:
	try:
		r = requests.get(jenkins_url + "computer/" + node + "/slave-agent.jnlp", allow_redirects=True, auth=auth)
		open(temp_path + 'slave-agent.jnlp', 'wb').write(r.content)
		tree = ET.parse(temp_path + 'slave-agent.jnlp')
		root = tree.getroot()
		secret = root[0][0].text
		#print (secret)
		flags = 0
		flags |= 0x00000008  # DETACHED_PROCESS
		flags |= 0x00000200  # CREATE_NEW_PROCESS_GROUP
		flags |= 0x08000000  # CREATE_NO_WINDOW
		pkwargs = {
			'close_fds': True,  # close stdin/stdout/stderr on child
			'creationflags': flags,
		}
		process = subprocess.Popen(['java', '-Xmx256m', '-jar', temp_path + 'agent.jar', '-jnlpUrl', jenkins_url + "computer/" + node + '/slave-agent.jnlp', '-secret', secret, '-workDir', 'c:/Jenkins'], start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **pkwargs)
		print(str(process.pid))
	except Exception as exc:
		print("Exception orrcured while connecting " + node + " - " + repr(exc))
