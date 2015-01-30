Exploring Paramiko's Errors
==========================

.. '




.. _paramiko-bad-hostname:

Bad Hostname
------------

What happens if you give it a bad host-name?


.. code:: python

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.load_system_host_keys()
    
    try:
        client.connect('badhostname', username='fakeuser')
    except IOError as error:
        print(error)

.. code::

    [Errno -2] Name or service not known
    



That is dissapointingly vague, but at least I know how to catch the exception (it's actually raising a `socket.error` but that's a child of IOError so you can catch either one). The error number is a system error number:


.. code:: python

    print("ENOENT: {0} '{1}'".format(errno.ENOENT, os.strerror(errno.ENOENT)))

.. code::

    ENOENT: 2 'No such file or directory'
    



.. currentmodule:: errno
.. autosummary::
   :toctree: api

   ENOENT

.. currentmodule:: os
.. autosummary::
   :toctree: api

   strerror

Looking at the documentation, though, it looks like it might make more sense to catch gaierror, not IOError.

.. currentmodule::
.. autosummary::
   :toctree: api

   socket.gaierror

But, that doesn't work, because the connect raises a ``socket.error`` instead.

.. '

.. _paramiko-bad-username:

Bad Username
------------

What happens if the address is okay but the user-name is wrong (it doesn't exist)?

.. '


.. code:: python

    try:
        client.connect('localhost', username='ummagumma')
    except paramiko.PasswordRequiredException as error:
        print(error)

.. code::

    Private key file is encrypted
    



So, there's three really bad things that happened here.

    * Ubuntu popped up a gui asking for the password for the private-key which will then block the code forever since there's no way to tell gnome what to do in the code.

    * Even though I typed in my password it rejected it.

    * The error message indicates that the private key is encrypted, even though it clearly isn't, given that I can ssh to real usernames. This seems like something that would be really hard to work around.

.. '


.. note:: By (re) moving /etc/xdg/autostart/gnome-keyring-ssh.desktop I was able to disable the pop-up and it now fails without user-interaction. I don't know how reasonable it is to expect that all users will know to do this, but at least it works.

.. '

.. _paramiko-bad-password:

Bad Password
------------

I assume that the bad username and the bad password errors will be the same, since it raised a `PasswordRequiredException`, but I guess it's better to test it and see.

.. '


.. code:: python

    try:
        client.connect('localhost', username='fakeuser', password='badpassword')
    except paramiko.AuthenticationException as error:
        print(error)

.. code::

    Authentication failed.
    



Ooops... okay so a bad password is an `AuthenticationException` but a bad username is a `PasswordRequiredException`.

.. note:: Once I killed the keyring the `PasswordRequiredException` popped up when I forgot to execute `ssh-add` so although the error string doesn't seem to be meaningful, the exception is -- it is raised if a password is needed and you didn't give it one (the bad username is then kind of a red-herring, ssh interprets it as a bad password).



.. _paramiko-socket-timeout:

Socket Timeouts
---------------

The last thing to check is the socket timeouts. These will pop up if you give paramiko a timeout and it's exceeded (surprised?).

.. '


.. code:: python

    client.connect('localhost', username='tester_tester', password=None)
    i,o,e = client.exec_command('ps -e | grep iperf')
    for line in o:
        pid = line.split()[0]
        client.exec_command('kill -9 {0}'.format(pid))
    time.sleep(0.1)
    
    stdin, stdout, stderr = client.exec_command('iperf -s', timeout=0.1)
    
    try:
        for line in stdout:
            print(line)
        for line in stderr:
            print(line)
    except socket.timeout as error:
        print( "socket.timeout doesn't give an error message")
        print( error)

.. code::

    ------------------------------------------------------------
    
    Server listening on TCP port 5001
    
    TCP window size: 85.3 KByte (default)
    
    ------------------------------------------------------------
    
    socket.timeout doesn't give an error message
    
    



.. _paramiko-stderr-checking:

On StandardError
----------------

When I was working with the previous section I initially forgot to kill the `iperf` process between runs of this code and was not getting any output because I wasn't checking stderr -- an error from the command won't raise an exception in paramiko, so to be safe you have to always check stderr. But also note that not all stderr output is an error:


.. code:: python

    stdin, stdout, stderr = client.exec_command('iperf -v')
    for line in stderr:
        print( line)

.. code::

    iperf version 2.0.5 (08 Jul 2010) pthreads
    
    



So it seems there is no universal way to decide if there was an error in the execution of the command -- you have to know what to expect and interpret it for each command.
