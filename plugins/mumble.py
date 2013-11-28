from util import hook, http

import re

@hook.command(autohelp=False)
def mumble(inp):
	".mumble <list>/<info> -- shows user list "

	userlist = re.match(r"^list$", inp)
	pastebin = re.match(r"^info$", inp)

# bad arg or need help
	
	if inp and userlist is None and pastebin is None:
		return mumble.__doc__
	elif pastebin:
		return "Mumble Info => http://pastebin.com/raw.php?i=vCTURaXQ"
	else:
		request_url = "http://mumble.valoryn.net:8081/stats"
		response = http.get_json(request_url)

		if response["serverInfo"] is None:
			return "mumble server API problem (scream obscenities at Mido until he cries and/or fixes)"

		if response["serverInfo"]["isRunning"] is False:
			return "mumble server is offline"

		# we want mumble user amount and info
		if not inp: 
			return "Mumble Status: " + str(response["serverInfo"]["userCount"]) + " people online."

		# we want list of usernames online
		if userlist: 
			return "Who's on Mumble: " + " ".join(response["serverInfo"]["userList"])