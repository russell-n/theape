Moving Thread Locks Close To the Problem
========================================

Contents:

    * :ref:`Introduction <exploring-thread-locks-introduction>`

    * :ref:`Methods <exploring-thread-locks-methods>`

    * :ref:`Results <exploring-thread-locks-results>`

    * :ref:`Discussion <exploring-thread-locks-discussion>`

.. _exploring-thread-locks-introduction:

Introduction
------------

In order to search for correlations between measured values (e.g. bitrate and throughput) I have in the past monitored multiple files and programs on devices using timestamps to correlate them later. Since monitoring has to be run in parallel to be useful I've used threads to run background processes in the background along with the primary one. One problem that arises in these situations is that threads have to call non-thread-safe methods (e.g. `paramiko's` ``SSHClient.exec_command``) and this can cause problems when called if the threads share the same object.

The primary solution to this problem has been to use different `SSHClient` instances -- and this has worked well. There have, however, been cases where the devices seemed to struggle under the load of having too many open processes. While I don't believe that eliminating ssh-sessions is necessarily the solution for these cases, I would like to have the option to run a single session shared by multiple threads.

My previous solution to providing a single instance in a safe way has been to share a lock among threads that share the ssh-session, but this seems to overly complicate things. My initial idea was to put the lock in the object that uses the non-thread-safe call so that the users of the holder of the ssh-session would not need to worry about it, but then I thought that it didn't seem likely that you could keep calling the same method object without the method finishing, so I decided to investigate what happens when you try. This is a record of what I found.

.. _exploring-thread-locks-methods:

Methods
-------

Two classes were created -- one with a ``run`` method that would would be shared among the threads. The ``run`` method will use a ``threading.Lock`` object to prevent multiple threads from being able to get to the second print statement within it.

::

    # python standard library
    import threading
    import time
    
    

::

    class Shared(object):
        def __init__(self):
            self.lock = threading.Lock()
            return
    
        def run(self, name):
            """
            :param:
    
             - `name`: identifier to use in print statements
            """
            print "{0} Acquiring Lock".format(name)
            with self.lock:
                print "{0} in Lock".format(name)
                # the sleep makes sure the calls to this method overlap
                time.sleep(2)
            print "{0} released Lock".format(name)
            return
    # end of class Shared    
    



The other class will be used to create the threads that use the ``Shared`` object.

::

    class Test(object):
        def __init__(self, name, target):
            """
            :param:
    
             - `name`: identifier to print in ``run`` calls
             - `target`: run method object
            """
            self.name = name
            self.target = target
            return
    
        def start(self):
            self.thread = threading.Thread(target=self.target,
                                           kwargs={'name':self.name})
            self.thread.daemon = True
            self.thread.start()
            return
    
        def join(self):
            self.thread.join()
            return
    # end class Test
    
    



.. _exploring-thread-locks-results:

Results
-------

One instance of the ``Shared`` class was created and its run method passed to ten instances of the ``Test`` class.

::

    s = Shared()
    tests = [Test("Test {0}".format(number), s.run) for number in range(10)]
    
    for test in tests:
        test.start()
    
    for test in tests:
        test.join()    
    
    

::

    Test 0 Acquiring Lock
    Test 0 in Lock
    Test 1 Acquiring Lock
    Test 2 Acquiring Lock
    Test 3 Acquiring Lock
    Test 4 Acquiring Lock
    Test 5 Acquiring Lock
    Test 6 Acquiring Lock
    Test 7 Acquiring Lock
    Test 8 Acquiring Lock
    Test 9 Acquiring Lock
    Test 0 released Lock
    Test 1 in Lock
    Test 1 released Lock
    Test 2 in Lock
    Test 2 released Lock
    Test 3 in Lock
    Test 3 released Lock
    Test 4 in Lock
    Test 4 released Lock
    Test 5 in Lock
    Test 5 released Lock
    Test 6 in Lock
    Test 6 released Lock
    Test 7 in Lock
    Test 7 released Lock
    Test 8 in Lock
    Test 8 released Lock
    Test 9 in Lock
    Test 9 released Lock
    
    



The ``Shared.run`` method was executed repeatedly even though previous calls weren't finished and then each waited for the previous call to finish before entering the protected area.

.. '

.. _exploring-thread-locks-discussion:

Discussion
----------

Since all calls to the same ``Shared.run`` method reached the first print statement before all calls were completed, it appears that python allows calling the same method object even prior to the completed execution of prior calls, at least in the case where everything within the method is thread-safe or protected by a lock. The output in this experiment indicated that the calls finished in order but the documentation notes that the order in which threads acquire the lock is not guaranteed. Given the outcome it is reasonable to use locks within method calls that need to protect non-thread-safe calls rather than requiring users of the object to maintain and use the lock -- in particular this can be used to protect ``SSHClient.exec_command`` calls.

There are drawbacks to this method. If the protected call takes an excessive time those waiting for it to finish will have extra (unpredictable) delays added to them.  Having the clients share the same method also makes the system brittle -- one failure affects all those that share it. Because of these drawbacks, in most cases it would seem to be better not to use resource-sharing unnecessarily, but since the call to the lock is relatively inexpensive, integrating it even though it won't be used for most cases seems to offer the advantage of lower-complexity to systems that don't need high-performance, which would likely include most cases where non-atomic calls need to be protected by a lock.

