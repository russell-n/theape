An Exec Command Example
=======================

.. _paramiko-sshclient-exec_command:

The SSHClient exec_command
--------------------------

Now that I've managed to get a connection going it's time to turn my attenttion to actually doing things on the machine. Paramiko has two ways to work with the shell -- interactively using ``invoke_shell`` and non-interactively using ``exec_command``. Since my intention is to use this within code I will focus on the ``exec_command`` method.

.. currentmodule:: paramiko.client
.. autosummary::
   :toctree: api
   
   SSHClient.exec_command
   SSHClient.invoke_shell

There's a few things of interest to note. One is that they've added a timeout so there's no need to sub-class it and add your own to get a timeout (assuming that what it's there for). The second thing to note is that it raises a `paramiko.SSHException` if the server fails to execute the command. Does this mean all errors? What if it's a connectivity problem, does it raise this instead of a `socket.error`? The third (and probably most immediately useful) thing to note is that what you get back is a tuple of (`stdin`, `stdout`, `stderr`). It's important to note the ordering of the returned tuples, as mixing them up will produce unpredictable results (I had standard out and standard in switched in one of the earlier examples and got an `IOError` when I tried to read from standard in -- the error said that the file was closed, which might make sense if you know that I was trying to read from standard in, but it took me a little while to figure it out).

.. _paramiko-exploration-nmap:

nmap
----

I want to see if paramiko will allow me to run commands as sudo. Since `nmap` will change its behavior (adding MAC addresses) if you run the ping-scan using `sudo` I can run it with and without root privileges and see if I get the expected output.

::

    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('localhost', username='fakeuser')
    stdin, stdout, stderr = client.exec_command("nmap -sP '192.168.103.*'")
    for line in stdout:
        print line
    

::

    
    
    Starting Nmap 6.00 ( http://nmap.org ) at 2013-11-04 11:50 PST
    
    Nmap scan report for 192.168.103.1
    
    Host is up (0.012s latency).
    
    Nmap scan report for acheron (192.168.103.15)
    
    Host is up (0.00057s latency).
    
    Nmap scan report for 192.168.103.16
    
    Host is up (0.00070s latency).
    
    Nmap scan report for 192.168.103.17
    
    Host is up (0.00069s latency).
    
    Nmap scan report for 192.168.103.19
    
    Host is up (0.026s latency).
    
    Nmap scan report for 192.168.103.20
    
    Host is up (0.00065s latency).
    
    Nmap scan report for 192.168.103.33
    
    Host is up (0.00073s latency).
    
    Nmap scan report for 192.168.103.50
    
    Host is up (0.00032s latency).
    
    Nmap done: 256 IP addresses (8 hosts up) scanned in 2.52 seconds
    
    



And now with sudo.

::

    stdin, stdout, stderr = client.exec_command('sudo nmap -sP "192.168.103.*"', get_pty=True)
    stdin.write('fakepassword\n')
    for line in stdout:
        print line    
    

::

    fakepassword
    
    [sudo] password for fakeuser: 
    
    
    
    Starting Nmap 6.00 ( http://nmap.org ) at 2013-11-04 11:50 PST
    
    Nmap scan report for 192.168.103.1
    
    Host is up (0.078s latency).
    
    MAC Address: 6C:41:6A:D8:90:47 (Unknown)
    
    Nmap scan report for acheron (192.168.103.15)
    
    Host is up (0.00018s latency).
    
    MAC Address: E8:E0:B7:A6:23:5F (Toshiba)
    
    Nmap scan report for 192.168.103.16
    
    Host is up (0.00015s latency).
    
    MAC Address: 70:5A:B6:23:6C:1F (Compal Information (kunshan) CO.)
    
    Nmap scan report for 192.168.103.17
    
    Host is up (0.00045s latency).
    
    MAC Address: D4:BE:D9:38:4B:0F (Dell)
    
    Nmap scan report for 192.168.103.19
    
    Host is up (0.095s latency).
    
    MAC Address: 00:BB:3A:AB:47:37 (Unknown)
    
    Nmap scan report for 192.168.103.20
    
    Host is up (0.00056s latency).
    
    MAC Address: 00:14:D1:B0:D5:F0 (Trendnet)
    
    Nmap scan report for 192.168.103.33
    
    Host is up (0.00040s latency).
    
    MAC Address: D4:BE:D9:5B:AE:4B (Dell)
    
    Nmap scan report for 192.168.103.50
    
    Host is up.
    
    Nmap done: 256 IP addresses (8 hosts up) scanned in 9.91 seconds
    
    



Two things to note -- one is that I didn't need to call the load_system_host_keys. It seems that the AutoAddPolicy takes care of that. The other thing to note is that I needed to set `get_pty` to True. If I didn't it would close the channel with this error (on my machine)::

    sudo: no tty present and no askpass program specified



