
BLUE = "\033[34m"
RED  = "\033[31m"
BOLD = "\033[1m"
RESET = "\033[0;0m"


TEMPLATE="""
{bold}Name{reset}
{{name}}

{bold}Synopsis{reset}
{{synopsis}}

{bold}Description{reset}
{{description}}

{bold}Examples{reset}
{{examples}}

{bold}See Also{reset}
{{see_also}}
""".format(bold=BOLD, reset=RESET)


NAME_TEMPLATE="{0}{{name}}{1} - {{description}}".format(BOLD, RESET)


name=NAME_TEMPLATE.format(name='cow', description='a cow says mu')
description="cow is a ruminant processor of grass to various useful products."
help_string  = TEMPLATE.format(name=name,
                        synopsis='cow [--moo]',                            
                        description=description,
                        examples='cow --moo mu',
                        see_also='pig, buffalo')
print help_string
