from urllib2 import urlopen
from json import load, dumps

def james(limit = 1, tag = 'james'):
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_first_photo():
    return james()['response'][0]['photos'][0]['original_size']['url']

if __name__ == '__main__':
    print dumps(james(), sort_keys=True, indent=4)
    print get_first_photo()
