The SSH Connection
==================

.. _ape-ssh-connection:

This is the workhorse connection built around the `paramiko` SSHClient. Updates in paramiko's interface as well as a better understanding of how it works has lead me to re-start it as the basis for the other connection types.

.. '



.. currentmodule:: ape.parts.connections.sshconnection
.. autosummary::
   :toctree: api

   SSHConnection

.. uml::

   SSHConnection -|> BaseClass
   SSHConnection o-- paramiko.SSHClient
   SSHConnection : sudo(command, password, [timeout=None])
   SSHConnection : __call__(command, [timeout=None, [get_pty=False]])
   SSHConnection : exec_command(command, [timeout=None, [get_pty=False]])
   SSHConnection : __getattr__(command, [timeout, [get_pty=False]])
   
