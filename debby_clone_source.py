
import subprocess
import os
import shutil

outcmd = subprocess.check_output(["apt", "list", '--installed'])
outcmd = [x for x in outcmd.decode().split('\n') if x]

osrelease = dict([x.strip().split('=') for x in open('/etc/os-release').readlines()])
codename = osrelease['VERSION_CODENAME']

native = ['amd64', 'all']

outpkgs = []
outpkgs_local = []

for x in outcmd:
	if x!='Listing...':
		splitv = x.split('/', 1)
		pkgname, state = splitv
		state = state.split(' ')
		if len(state)>3:
			pkgarch = state[2]
			pngins = state[3][1:-1].split(',')

			if 'automatic' not in pngins:
				outname = pkgname
				if pkgarch not in native: outname += ':'+pkgarch
				(outpkgs_local if 'local' in pngins else outpkgs).append(outname)

if not os.path.exists('migration_data'):
    os.makedirs('migration_data')

f = open('migration_data/codename.txt', 'w')
f.write(codename)
f.flush()
f.close()

f = open('migration_data/packages.txt', 'w')
for x in outpkgs: f.write(x+'\n')
f.flush()
f.close()

f = open('migration_data/packages_local.txt', 'w')
for x in outpkgs_local: f.write(x+'\n')
f.flush()
f.close()

keyf = 'migration_data/'+codename

if not os.path.exists(keyf): os.makedirs(keyf)

shutil.copy('/etc/apt/sources.list', keyf+'/sources.list')
shutil.copytree('/etc/apt/keyrings/', keyf+'/apt_keyrings', dirs_exist_ok=True)
shutil.copytree('/etc/apt/trusted.gpg.d/', keyf+'/apt_trusted', dirs_exist_ok=True)
shutil.copytree('/etc/apt/sources.list.d/', keyf+'/apt_sources', dirs_exist_ok=True)
shutil.copytree('/usr/share/keyrings/', keyf+'/share_keyrings', dirs_exist_ok=True)