
import subprocess
import os
import shutil

osrelease = dict([x.strip().split('=') for x in open('/etc/os-release').readlines()])
codename_target = osrelease['VERSION_CODENAME']

keyf = 'migration_data/'

DEBUG = 1

codename_source = open(keyf+'codename.txt', 'r').read()
packages = open(keyf+'packages.txt', 'r').read().split('\n')
packages = [x.split(':') for x in packages]

global_sources = [
'brave-browser-release.sources',
'drdteam-amd64.sources',
'Floorp.list',
'google-chrome.sources',
'google-earth-pro.list',
'kxstudio-debian-ppas-2.list',
'kxstudio-debian-ppas.list',
'microsoft-edge.sources',
'opera-gx-stable.list',
'opera-stable.list',
'sublime-text.sources',
'vivaldi.sources',
]

if not DEBUG:
	shutil.copytree(keyf+'/apt_keyrings/', '/etc/apt/keyrings/', dirs_exist_ok=True)
	shutil.copytree(keyf+'/apt_trusted/', '/etc/apt/trusted.gpg.d/', dirs_exist_ok=True)
	shutil.copytree(keyf+'/share_keyrings/', '/usr/share/keyrings/', dirs_exist_ok=True)
	if codename_source==codename_target:
		shutil.copy(keyf+'/sources.list', '/etc/apt/sources.list')
		shutil.copytree(keyf+'/apt_sources/', '/etc/apt/sources.list.d/', dirs_exist_ok=True)
	else:
		for n in global_sources:
			infile = keyf+'/apt_sources/'+n
			if os.path.exists(infile):
				shutil.copy(infile, '/etc/apt/sources.list.d/')

allpkg = []

#subprocess.check_output(["apt", "update"])
outcmd = subprocess.check_output(["apt", "list"])
outcmd = [x for x in outcmd.decode().split('\n') if x]
for x in outcmd:
	if x!='Listing...':
		splitv = x.split('/', 1)
		allpkg.append(splitv[0])

packages = [x[0] for x in packages if len(x)==1]
foundpkgs = [x for x in packages if x in allpkg]
missingpkgs = [x for x in packages if x not in allpkg]

f = open('install.sh', 'w')
f.write('apt install '+' '.join(foundpkgs))
f.flush()
f.close()

f = open('missing_packages.txt', 'w')
for x in missingpkgs: f.write(x+'\n')
f.flush()
f.close()

subprocess.check_output(["chmod", "+x", "install.sh"])