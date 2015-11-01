import time
import re
import redis
import os

crontable = []
outputs = []
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379') # read from env variables on server

def process_message(data):
	# this plug in will match any message that has <user>** and output a message
	print '---- %s' % data
	
	text = data.get('text')
	message_type = data.get('type')
	team = data.get('team')
	if text and message_type and team:
		result = re.search('\<@.+\>\+{2}', text)
		# rd = redis.StrictRedis()
		rd = redis.from_url(redis_url)
		if result and message_type == 'message':

			user = text[text.rfind('<@')+2: text.rfind('>')]
			vote = text[text.find('++'):text.find('++')+2 ]
			score = rd.incr('user:%s:%s' % (team, user))
			outputs.append([data['channel'], "<@%s>%s [hooray, you scored: %s]" % (user, vote, score)])
			# outputs.append([data['channel'], "from repeat1 \"{}\" in channel {}".format(data['text'], data['channel']) ])

