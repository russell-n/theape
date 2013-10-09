
# this package 
from base_plugin import BasePlugin
from constants import TEMPLATE, NAME_TEMPLATE, BLUE, RESET, RED


EXAMPLES = '''
arachneape run ape.ini
arachneape help
arachneape fetch
arachneape list'''

class ArachneApe(BasePlugin):
    """
    The default plugin
    """
    @property
    def help(self):
        """
        A help-string to print
        """
        if self._help is None:            
            description = "A builder for the arachneape run strategy."
            formatted_name = "{b}{n}{r}".format(b=BLUE,
                                                n=self.__class__.__name__,
                                                r=RESET)
            name = NAME_TEMPLATE.format(name=formatted_name,
                                        description=description)

            description = "{b}ArachneApe{r} is a code-runner whose execution is declared in a configuration file (or list of configuration files) that it reads at run-time. Within the {red}[ARACHNEAPE]{r} section of the configuration file you declare the plugins that you want to execute. The rest of the configuration file depends on the plugins you declare so you will need to check with them individually.".format(b=BLUE, r=RESET, red=RED)
            
            self._help = TEMPLATE.format(name=name,
                                        description=description,
                                        synopsis='arachneape run [config-file-glob]',
                                        examples = EXAMPLES,
                                        see_also = "ape, arachne")
        return self._help
    
    @property
    def product(self):
        """
        this is a product
        """
        return
# end class ArachnePlugin        
