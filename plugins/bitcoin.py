from util import http, hook


@hook.command(autohelp=False)
def bitcoin(inp, nick=''):
    ".bitcoin -- do never buy"
    return "stop asking about bitcoins you idiot."