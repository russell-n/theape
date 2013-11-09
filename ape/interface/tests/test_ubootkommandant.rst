Testing The UbootKommandant
===========================

Once again, having the testing in the same modules as the code is causing the auto-generated module diagrams to get too big so this is moved outside.

::

    # python standard library
    import unittest
    
    # third-party
    from mock import MagicMock, patch
    
    # this package
    from ape.interface.ubootkommandant import UbootKommandant
    



