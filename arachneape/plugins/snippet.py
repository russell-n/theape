import textwrap
import shlex
import subprocess

tw = textwrap.TextWrapper(width=40, subsequent_indent=' ' * 5)
text = """
A Little Text:

Now is the winter of our discontent;
Made glorious summer by this Son of York;
And all the clouds that lour'd upon our house;
In the deep bosom of the ocean buried.
"""
long_text = text * 100
wrapped_text = tw.fill(long_text)
command = shlex.split('echo "{0}" | less -R'.format(wrapped_text))

# this goes to stdout so it won't show up in the documentation
subprocess.check_call(command)

#subprocess.Popen('less -R'.split(), stdin=subprocess.PIPE).communicate(input=wrapped_text)
