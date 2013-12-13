import re

from util import hook


@hook.command(autohelp=False)
def games(inp, bot=None, pm=None):
    ".games -- links to google doc of SAGameDev games"

    pm('https://docs.google.com/spreadsheet/ccc?key=0AhjIgG_DsNePdHNwLXRGVHJDR1FzdC1EUV9sSTNoUlE&usp=sharing')