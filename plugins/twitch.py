from util import hook, http

import re
import urllib2

@hook.command(autohelp=False)
def twitch(inp, db=None):
    ".twitch /.twitch <add>/<remove> <twitchaccount> -- for SAGameDev streamers"

    db.execute("create table if not exists twitch (account STRING PRIMARY KEY)")
    db.commit()

    add = re.match(r"^add\s(\w+)$", inp)
    remove = re.match(r"^remove\s(\w+)$", inp)

    # we want the multitwitch link
    if not inp:
    	return get_multitwitch_url(db)
    # we want to add a stream
    elif add:
    	unicode_user = add.groups()[0]
    	return add_stream(unicode_user.encode('ascii'),db)
    # we want to remove a stream
    elif remove:
    	unicode_user = remove.groups()[0]
    	return remove_stream(unicode_user.encode('ascii'),db)
    # bad arg (or .twitch help)
    else:
    	return twitch.__doc__

def get_help():
	return twitch.__doc__

def get_multitwitch_url(db):
	streams = db.execute("select * from twitch").fetchall()

	if not streams:
		return "no streams on watch list"
	else:
		print len(streams)
		stream_list = ""
		for user_raw in streams:
			user = user_raw[0].encode('ascii')

			if is_online(user):
				if stream_list:
					stream_list += "/"
				stream_list += user

		if not stream_list:
			return "nobody from SAGameDev is streaming right now (.twitch help -- shows commands)"
		else:
			multitwitch = "http://multitwitch.tv/"
			multitwitch += stream_list
			return multitwitch + " (.twitch help -- shows commands)"

def is_online(stream):
	request_url = "https://api.twitch.tv/kraken/streams/%s" % stream
	response = http.get_json(request_url)
	return response["stream"] is not None

def add_stream(stream, db):
	exists = db.execute("select account from twitch where account=?", (stream,)).fetchone()
	if not exists:
		message = is_valid_stream(stream)
		if message:
			return message
		else:
			db.execute("insert into twitch(account) values(?) ",(stream,))
			db.commit()
			return "added " + stream + " stream to watched list"
	else:
		return stream + "'s stream is already on watch list"

# returns error message if not valid else empty string
def is_valid_stream(stream):
	request_url = "https://api.twitch.tv/kraken/streams/%s" % stream
	try:
		response = http.get_json(request_url)
	except urllib2.HTTPError, err:
		if err.code == 404:
			return stream + " is not a valid account on twitch.tv. (not added)"
		elif err.code == 422:
			return stream + " is a justin.tv account. (not added)"
		else:
			return str(err.code) + " received, tell poem to deal with it."

def remove_stream(stream, db):
	db.execute("delete from twitch where account=?",(stream,))
	db.commit()
	return stream + "'s stream removed from watch list"