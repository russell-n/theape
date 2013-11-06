The SSH Connection
==================

.. _ape-ssh-connection:

This is the workhorse connection built around the `paramiko` SSHClient. Updates in paramiko's interface as well as a better understanding of how it works has lead me to re-start it as the basis for the other connection types.

.. '





.. currentmodule:: ape.parts.connections.sshconnection
.. autosummary::
   :toctree: api

   SSHConnection
   SSHConnection.client
   SSHConnection.sudo
   SSHConnection.__call__

.. uml::

   SSHConnection -|> BaseClass
   SSHConnection o-- paramiko.SSHClient
   SSHConnection o-- SocketStorage
   SSHConnection : sudo(command, password, [timeout=None])
   SSHConnection : __call__(command, [timeout=None, [get_pty=False]])
   SSHConnection : exec_command(command, [timeout=None, [get_pty=False]])
   SSHConnection : __getattr__(command, [timeout, [get_pty=False]])

.. _ape-sshconnection-client:

The SSHClient
-------------

Behind the scenes this is mostly a thin adapter for the SSHClient.

.. currentmodule:: paramiko.client
.. autosummary::
   :toctree: api

   SSHClient

And the methods are versions of the `exec_command`.

.. currentmodule:: paramiko.client
.. autosummary::
   :toctree: api

   SSHClient.exec_command

.. _ape-sshconnection-inouterror:
   
The InOutError Named Tuple
--------------------------

To help prevent the mixing up of the different files returned (stdout, stdin, and stderr (not necessarily in that order)) the SSHConnection will returned a named tuple.



.. uml::

   InOutError -|> collections.namedtuple
   InOutError : Storage input
   InOutError : Storage output
   InOutError : Storage error
