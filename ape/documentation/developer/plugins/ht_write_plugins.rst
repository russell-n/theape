How to Write Plugins
====================

.. Audience: Future plugin writers
.. Context: Current system has a rudimentary plugin system but trying to read the example code to figure out how to build a new one is too hard.
.. Topic: APE Plugins
.. Question: How do you create new plugins for the APE?
.. Relevance: Need to understand how plugin creation works to maintain current code and create new plugins.
.. Thesis: By following the basic set of steps a plugin for the ape can be created.

One of the key features that sets this version of the APE apart from prior ones is the use of `plugins` to extend its operation. Actually creating one is relatively simple, but it can be confusing when looking at the existing plugins as they have a lot of extra text meant to help the end-user. This document shows that by following a 5-step procedure you can create a plugin which can then be auto-discovered by the APE to use. Although creating the plugin itself is relatively simple, the interaction of multiple parts can get complicated once you start doing more complicated things like connecting a client and server so for this example I'll use the Sleep plugin as an example since it is self-contained.

.. '

Procedure
---------

There are 5 steps needed to create a plugin:

   1. :ref:`Import the *BasePlugin* and whatever is needed to build the parts of the plugin <ht-write-plugin-import>`

   2. :ref:`Create an example configuration string that the user can base a configuration file on <ht-write-plugin-configuration>`

   3. :ref:`Create a Help Dictionary <ht-write-plugin-help>`

   4. :ref:`Implement the plugin <ht-write-plugin-implement>`

   5. :ref:`Put the plugin somewhere it can be imported <ht-write-plugin-install>`

There are other steps like planning and testing, but since the plugins don't do anything other than build and bundle other code, any other steps will be specific to the plugin created. I'll work through the steps, using the :ref:`SleepPlugin <sleep-plugin>` which is one of the plugins that comes with the ape (it's in the `plugin` folder -- ``ape.plugins.sleep_plugin``) as a concrete example. The `SleepPlugin` is a plugin for :ref:`TheBigSleep <ape-big-sleep>`, a stand alone part that takes a time-string and sleeps when called.

.. '

.. uml::

   Component <|-- TheBigSleep
   TheBigSleep : __init__(end, total, interval, verbose)
   TheBigSleep : __call__()
   BasePlugin <|-- Sleep
   Sleep o- TheBigSleep
   Sleep : fetch_config()
   Sleep : Dict sections
   Sleep : TheBigSleep product

.. currentmodule:: ape.plugins.base_plugin
.. autosummary::
   :toctree: api

   BasePlugin
   
.. currentmodule:: ape.parts.sleep.sleep
.. autosummary::
   :toctree: api

   TheBigSleep

.. currentmodule:: ape.plugins.sleep_plugin
.. autosummary::
   :toctree: api

   Sleep

.. _ht-write-plugin-import:   
   
1. Import What You Need
~~~~~~~~~~~~~~~~~~~~~~~

In order to be recognized by the APE your plugin has to inherit from the :ref:`BasePlugin <base-plugin>` so you will need to import it along with the parts that are composed within your plugin::

    # This package
    from ape import BasePlugin
    from ape.parts.sleep.sleep import TheBigSleep

In addition, the Help section of the plugin uses the keys of a dictionary when building the help string so I like to use an ordered dictionary so I can control what order the sections appear in::

    # python standard library
    from collections import OrderedDict

.. _ht-write-plugin-configuration:    

2. Create an example configuration file snippet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The expected way for a user to get a sample configuration file is to use the ``fetch`` sub-command::

    ape fetch <plugin name>

Where ``<plugin name>`` is the name of sume plugin. When this sub-command is issued, the ape will build the plugin and call its ``fetch_config`` method, which should return a string with the sample configuration to the APE. As an example, if the user entered ``ape fetch Sleep``, the following should be returned:

.. code-block:: ini

    [SLEEP]
    # 'end' should be a timestamp for the end-time (11-12-2013 8:45 pm)
    # 'total' should be a timestamp for the run-time (1 hr 23 minutes)
    # 'interval' should be <amount> <units> (1 minute)
    # if verbose is False, sceen output will be off except at startup
    # only one of absolute or relative time is required, although both can be used
    end = <absolute time>
    total = <relative time>
    interval = 1 second
    verbose = True

Since the configuration-file is read-in using python's `ConfigParser <http://docs.python.org/2/library/configparser.html>`_, the sample needs to be in the `ini` format. This string could be created in the plugin itself, but I like to create it outside to make it easier to separate the parts that go into the plugin. Here's more-or-less what's in the `sleep_plugin` module::

    SLEEP_SECTION = 'SLEEP'
    END_OPTION = 'end'
    TOTAL_OPTION = 'total'
    INTERVAL_OPTION = 'interval'
    VERBOSE_OPTION = 'verbose'
    
    configuration = """
    [{0}]
    # 'end' should be a timestamp for the end-time (11-12-2013 8:45 pm)
    # 'total' should be a timestamp for the run-time (1 hr 23 minutes)
    # 'interval' should be <amount> <units> (1 minute)
    # if verbose is False, sceen output will be off except at startup
    # only one of absolute or relative time is required, although both can be used
    {1} = <absolute time>
    {2} = <relative time>
    {3} = 1 second
    {4} = True
    """.format(SLEEP_SECTION, END_OPTION,
               TOTAL_OPTION,
               INTERVAL_OPTION,
               VERBOSE_OPTION)

.. '

The use of the constants (like `END_SECTION`) might seem wasteful, but I use them both in the sample and later when I parse the configuration so having them all in one place makes it easier in case I decide to rename things.

.. _ht-write-plugin-help:

3. Create a help dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide an online help system the plugin should create a dictionary of `<section-name>:<section contents>` pairs. The idea is to provide something like a man-page. As an example, I'll create an ordered dictionary called ``sections`` and add the ``name`` section to it::

    sections = OrderedDict()
    sections['name'] = '{bold}sleep{reset} -- a countdown timer that blocks until time is over'

.. '

The key `name` will appear in bold as will the word `sleep` in the matching text. In the background the APE will be using string formatting to add the ASCII codes for the formatting (in this case the `{bold}` and `{reset}`). The ``{reset}`` turns of any prior formatting so there should always be a `format-reset` pair or the formatting won't get turned off. Right now the only supported formating keywords are:

   * bold
   * blue
   * red

.. '

The rest of the help dictionary was created by adding more sections::

    sections['description'] = '{bold}sleep{reset} is a verbose no-op (by default) meant to allow the insertion of a pause in the execution of the APE. At this point all calls to sleep will get the same configuration.'
    sections['configuration'] = configuration
    sections['see also'] = 'EventTimer, RelativeTime, AbsoluteTime'
    sections['options'] = """
    The configuration options --
    
        {bold}end{reset} : an absolute time given as a time-stamp that can be interpreted by `dateutil.parser.parse`. This is for the cases where you have a specific time that you want the sleep to end.
    
        {bold}total{reset} : a relative time given as pairs of '<amount> <units>' -- e.g. '3.4 hours'. Most units only use the first letter, but since `months` and `minutes` both start with `m`, you have to use two letters to specify them. The sleep will stop at the start of the sleep + the total time given.
    
        {bold}interval{reset} : The amount of time beween reports of the time remaining (default = 1 second). Use the same formatting as the `total` option.
    
        {bold}verbose{reset} : If True (the default) then report time remaining at specified intervals while the sleep runs.
    
    One of {bold}end{reset} or {bold}total{reset} needs to be specified. Everything else is optional.
    """
    sections['author'] = 'ape'

To see how this was output type out the help sub-command for sleep::

    ape help Sleep

Since the output goes through a pager (`less`) I can't show the output here. Also note that the command is case-sensitive so ``ape help sleep`` will fail.

.. '

.. _ht-write-plugin-implement:

4. Implement the plugin
~~~~~~~~~~~~~~~~~~~~~~~

There are four parts to implementing the plugin:

    1. :ref:`Sub-class the BasePlugin <ht-write-plugin-subclass-baseplugin>`

    2. :ref:`Implement the fetch_config method <ht-write-plugin-implement-fetch-config>`

    3. :ref:`Implement the sections property <ht-write-plugin-implement-sections>`

    4. :ref:`Implement the product property <ht-write-plugin-implement-product>`

.. _ht-write-plugin-subclass-baseplugin:    

4.1 Sub-class the ``BasePlugin``
++++++++++++++++++++++++++++++++

The way the plugin discovery works is that the :ref:`QuarterMaster <quarter-master>` looks in the `plugins` folder (or other modules passed in at run-time) for classes that are sub-classed from the ``ape.BasePlugin`` so anything that needs to be auto-discovered has to be a ``BasePlugin`` child::

    class Sleep(BasePlugin):
        """
        A plugin for TheBigSleep
        """
        def __init__(self, *args, **kwargs):
            """
            Constructor for Sleep
            """
            super(Sleep, self).__init__(*args, **kwargs)
            return

The use of ``*args, **kwargs`` is so that the ``BasePlugin`` can have the :ref:`ConfigurationMap <configuration-map>` and the expected section-name from the config-file passed to it -- so every plugin should expect that it will have these attributes to use when building the `product`.

.. _ht-write-plugin-implement-fetch-config:

4.2 Implement the `fetch_config` method
+++++++++++++++++++++++++++++++++++++++

When a user types ``ape fetch <plugin>`` the APE calls the plugin's ``fetch_config`` method to get the configuration string and (currently) sends it to stdout. In the case of our example `Sleep` plugin we already have a `configuration` variable which holds the string so we can just have the `Sleep` print it::

    def fetch_config(self):
        """
        prints a config-file sample
        """
        print configuration

This might seem excessive but the original APE saved the configuration to a file rather than sending to stdout which made it likely that a user would accidentally destroy a prior configuration so this method was created to allow the way the `fetch` sub-command is handled to be changed.

.. '

.. _ht-write-plugin-implement-sections:

4.3 Implement the `sections` property
+++++++++++++++++++++++++++++++++++++

When a user calls the ``ape help <plugin>`` sub-command, the APE sends the plugin's `sections` property to the ``less`` command. So to make it work for our `Sleep` plugin we can assign it the ``sections`` dictionary that we created earlier::

    @property
    def sections(self):
        """
        Help dictionary
        """
        if self._sections is None:
            self._sections = sections
        return self._sections

.. '

.. _ht-write-plugin-implement-product:

4.4 Implement the `product` property
++++++++++++++++++++++++++++++++++++

The `product` is the object that the APE will call when the program is run (``ape run``). This means that the `product` has to be a callable-object that can be fully configured by the plugin (because no parameters will be passed in to the call). In the case of our example we know that we want to return the `TheBigSleep` object::

    @property
    def product(self):
        """
        A built TheBigSleep object

        :return: TheBigSleep
        """
        if self._product is None:
            end = self.configuration.get_datetime(section=self.section_header,
                                                  option=END_OPTION,
                                                  optional=True)
            total = self.configuration.get_relativetime(section=self.section_header,
                                                    option=TOTAL_OPTION,
                                                    optional=True)
            interval = self.configuration.get_relativetime(section=self.section_header,
                                                           option=INTERVAL_OPTION,
                                                           optional=True,
                                                           default=1)
            if interval != 1:
                interval = interval.total_seconds()
            verbose = self.configuration.get_boolean(section=self.section_header,
                                                     option=VERBOSE_OPTION,
                                                     optional=True,
                                                     default=True)
            self._product = TheBigSleep(end=end,
                                        total=total,
                                        interval=interval,
                                        verbose=verbose)
        return self._product


As you can see, it uses the ``self.section_header`` attribute that it inherits from the ``BasePlugin`` in order to know what the name of the section-header in the configuration file should be. In the default configuration the header is ``SLEEP`` but in order for a plugin to be used with more than one set of configurations (so that it can have more than one set of behaviors) I needed to allow the specifying of section headers.

The ``product`` builder, by and large, just calls the ConfigurationMap (`self.configuration`) and passes in the parameters to the object it's building. Hopefully the calls being made are obvious enough but if not the API might help explain what's being passed into the ``TheBigSleep`` constructor.

.. currentmodule:: ape.interface.configurationmap
.. autosummary::
   :toctree: api

   ConfigurationMap
   ConfigurationMap.get_datetime
   ConfigurationMap.get_boolean
   ConfigurationMap.get_relativetime

At this point we've  implemented the plugin, all that's required for it to be usable is that it be placed somewhere the APE can find it.

.. _ht-write-plugin-install:

5. Install the Plugin
~~~~~~~~~~~~~~~~~~~~~

In order for the APE to find a plugin two conditions need to be met:

   1. The plugin has to sub-class the `BasePlugin`
   2. The module with the plugin has to be known to the APE as a plugin source

In the case of the `Sleep` plugin it is part of the APE so it sits in the `ape.plugins` folder (the default place the APE looks for plugins). For non-ape plugins the package they belong to has to be installed (e.g. with `setup.py`) and the module name passed in to the APE on the command line.

Let's suppose that instead of the default `Sleep` plugin you made a better one called `BetterSleep` that's in the `bettersleep` package. Once the `bettersleep` package is installed then the user can access it using the ``--modules`` flag.

To see what plugins the APE recognizes in the module::

    ape list --modules bettersleep

To fetch the configuration snippet::

    ape fetch --modules bettersleep BetterSleep

To run::

    ape run --modules bettersleep

This requires that the user know what modules contain plugins so it isn't an automatic system, but I'm assuming that these cases will be rare enough that this will work. For non-APE maintainers it would make sense just to put the plugin in the APE's pluging folder, the external module solution is so that I can build and use plugins for code that won't be added to the APE itself.
