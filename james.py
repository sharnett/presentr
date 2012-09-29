from urllib2 import urlopen
from json import load, dumps

key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&api_key=%s'
limit = 1
tag = 'james'

james = load(urlopen(url % (tag, limit, key)))

print dumps(james, sort_keys=True, indent=4)

