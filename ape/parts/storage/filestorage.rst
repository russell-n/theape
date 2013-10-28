File Storage
============

This is a module for classes that implement a file-like interface to disk-files but also add some extra features meant to make them easier to use within the APE.

Contents:

    * :ref:`FileStorage Model <file-storage-model>`
    * :ref:`Extras <file-storage-extras>`
    * :ref:`Sub-Folders <file-storage-sub-folders>`
    * :ref:`Redundant Files <file-storage-redundant-files>`
    * :ref:`FileStorage API <file-storage-apy>`



.. _file-storage-model:

FileStorage Model
-----------------

Since the ultimate model for all storage classes is ``__builtin__.file`` (see: :ref:`exploring files <exploring-files>` for the API and some notes), this class will implement all the non-optional methods and attributes. In addition it will inherit from the :ref:`Composite <composite-class>` in order to allow non-homogeneous storage (e.g. stdout and disk -- the equivalent of the unix `tee`).

.. uml::

   FileStorage : FileStorage __init__(path, [,mode])
   FileStorage : open(name[, mode])
   FileStorage : close()
   FileStorage : flush()
   FileStorage : String read()
   FileStorage : String readline()
   FileStorage : List readlines()
   FileStorage : write(text)
   FileStorage : writeline(text)
   FileStorage : writelines(list)
   FileStorage : closed
   FileStorage : mode
   FileStorage : name
   FileStorage : path
   FileStorage : add(component)
   FileStorage : components
   FileStorage : __enter__
   FileStorage : __exit__
   FileStorage : __iter__

.. _file-storage-extras:

Extras
------

Although the built-in ``file`` is the model for the ``FileStorage``, it wouldn't make much sense to replicate it exactly. The main impetus for creating this (besides keeping an eye on non-disk output in the future) is to have something that can keep track of extra persistent data -- in particular:

   * Sub-folders 
   * Existing files with redundant names (and how to handle them)
   * Time-stamps

.. superfluous '   

.. _file-storage-sub-folders:

Sub-Folders
-----------

In order to help tame the explosion of files that can often happen from the repeated execution of code that collects data the FileStorage will accept a path which it will then prepend to any file-name when it is opened. If the sub-folder does not exist it will be created.

::

    example_path = 'aoeu/snth'
    example_file = 'umma.gumma'
    
    # this will be run multiple times, remove the example so it gets started fresh
    if os.path.isdir(example_path):
        shutil.rmtree(example_path)
    
    # this is the part that should be part of the path property
    if not os.path.isdir(example_path):
        os.makedirs(example_path)
    for name in os.listdir('aoeu'):
        print name
    

::

    snth
    



.. _file-storage-redundant-files:

Redundant Files
---------------

It often happens that data-collecting code will be run multiple times. The two ways proposed to avoid inadvertently overriding files are:

     * Appending count-numbers (e.g. a_0.txt, a_1.txt)
     * Adding Timestamps

The first scheme is more easily generalizable, while the second adds more useful information. It will therefore be assumed that both will be implemented and the increment scheme will only come into effect in the cases where the two files of the same name have been requested in too short a time-interval for the timestamps to differentiate them.

.. _file-storage-api:

FileStorage API
---------------

.. currentmodule:: ape.parts.storage.filestorage
.. autosummary::
   :toctree: api

   FileStorage   

