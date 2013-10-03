Plugin Constants
================

This holds constants for the plugins. Primarily the help-string components.

Font Constants
--------------

ASCII codes are used to change the text sent to standard output. The available codes are:

   * BLUE
   * RED
   * RESET
   * BOLD

* RESET gets rid of the previously set codes (it turns off bold and makes the color black).
* These codes are used in the TEMPLATE so you can use them but it is not required.



The Help Template
-----------------

The TEMPLATE string is set up to be used with string formatting and has the following named placeholders in the string:

.. csv-table:: Template Properties
   :header: Name, Meaning

   name, the subject of the help
   synopsis, the terse version of the description
   description, a more detailed description
   examples, examples of how to use the code
   see_also, references to other code that might be related



The Name Template
-----------------

This is an optional template to format the name you give to the TEMPLATE. it takes two named format options -- `name` and `description`. An example use::

   description='an interface to the on-line reference manuals'
   name_string = NAME_TEMPLATE.format(name='man', description=description)
                                      



An example use:

::

    name=NAME_TEMPLATE.format(name='cow', description='a cow says mu')
    description="cow is a ruminant processor of grass to various useful products."
    help_string  = TEMPLATE.format(name=name,
                            synopsis='cow [--moo]',                            
                            description=description,
                            examples='cow --moo mu',
                            see_also='pig, buffalo')
    print help_string
    

::

    
    [1mName[0;0m
    [1mcow[0;0m - a cow says mu
    
    [1mSynopsis[0;0m
    cow [--moo]
    
    [1mDescription[0;0m
    cow is a ruminant processor of grass to various useful products.
    
    [1mExamples[0;0m
    cow --moo mu
    
    [1mSee Also[0;0m
    pig, buffalo
    
    

