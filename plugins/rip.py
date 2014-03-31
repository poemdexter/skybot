from util import hook, strip_formatting
from textwrap import wrap

WIDTH = 40

@hook.command(autohelp=False)
def rip(inp, nick=''):
    if inp == '': return
    return "stop rippin you idiot."
