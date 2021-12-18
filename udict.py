import requests

def get_definitions(tag):
	tag = tag.replace(' ', '+')
	url = 'http://api.urbandictionary.com/v0/define?term=%s'
	result = requests.get(url % tag)
	defns = []

	for i in range(3):
		try:
			defns.append(result.json()['list'][i]['definition'])
		except IndexError as KeyError:
			break

	# padding:
	if len(defns) == 2:
		defns += ['This is everything mankind knows about %s.' % tag]
	elif len(defns) == 1:
		defns += ['Little more is known of this %s you speak of.' % tag]
		defns += ['Hello World.']
	elif len(defns) == 0:
		defns += ['Well done.']
		defns += ['Urban Dictionary has not even heard of this %s you speak of.' % tag]
		defns += ['Hello World.']
	return defns

if __name__ == '__main__':
	tag = input('topic: ')	
	definitions = get_definitions(tag)
	for d in definitions:
		print(d)
