Testing the ArgumentClinic
==========================

This proved to require more work than I wanted to spend so it is largely incomplete.

::

    # python standard library
    import unittest
    import random
    import argparse
    
    # third-party
    from mock import MagicMock, patch
    
    # this package
    from ape.interface.arguments import ArgumentClinic
    



