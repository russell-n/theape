The MacDut Bug
==============

Looking at the `setup.py` file shows that the code installs a command `automationRunner` that calls `AutomationSuite.runner.main'.

::

    print subprocess.check_output(shlex.split('automationRunner -h'))
    
    

::

    Usage: automationRunner [options] file.ini
    
    Options:
      -h, --help   show this help message and exit
      -e           Generate example.ini
      -o           Generate options.ini
      -d, --debug  Turn on debugging
    
    
    



Inside `runner.py` these lines appear to be the ones that run the RvR code that I've been asked to troubleshoot::

    from configobj import ConfigObj
    import AutomationSuite.AutomatedRVRgather as AutomatedRVRgather
    config = ConfigObj(args[0])
    test_object = AutomatedRVRgather.GatherTest(config['RvR'], options.debug)
    test_object.RunTest()

``args[0]`` is the '.ini' file name and ``options.debug`` is True if the debug flag was set in the command line arguments so we should be able to get the same effect using::

    config = ConfigObj('rvr.ini')
    test_object = AutomatedRVRgather.GatherTest(config['RvR'], False)
    test_object.RunTest()

Assuming that the configuration file is named 'rvr.ini'. That is the theory. Of course, I don't have an attenuator or any devices so this is going to be kind of ugly to work around.

.. superfluous '

What happens if you just naively call it?

::

    from configobj import ConfigObj
    import AutomationSuite.AutomatedRVRgather as AutomatedRVRgather
    
    config = ConfigObj('rvr.ini')
    
    #test_object = AutomatedRVRgather.GatherTest(config['RvR'], False)
    #test_object.RunTest()
    



Well, what happens is the paramiko client hangs up since I don't have anything on the network for it so I'm going to have to mock it out.


::

    from mock import MagicMock, patch
                
    
    ssh_mock = MagicMock()
    patcher = patch('paramiko.SSHClient')
    ssh_connection = patcher.start()
    try:
        test_object = AutomatedRVRgather.GatherTest(config['RvR'], False)
    except NameError as error:
        print_traceback(error)
    

::

    1383096549.594887 INFO Setting up tests
    1383096549.596150 INFO Setting up DUT and IperfGatherer
    Failed Line: 'if re.search("Darwin", os):'
    In Function: __Connected
    In File: MacDut.py
    At Line: 58
    



Well, it appears that the MacDut class has an error in it (undeclared (actually mis-named) variable).
