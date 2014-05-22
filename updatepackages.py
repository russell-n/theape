import subprocess

output = subprocess.check_output('pip list --outdated'.split())

for line in output.split('\n'):
    try:
        package = line.split()[0]
        print "Upgrading '{0}'".format(package)
        subprocess.check_call('pip install {0} --upgrade'.format(package).split())
    except (IndexError, subprocess.CalledProcessError) as error:
        print error
        

