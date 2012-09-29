from urllib2 import urlopen
from json import load, dumps

def james(limit = 1, tag = 'james'):
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(limit = 1):
    pass
    response = james(limit = limit)['response']
    photos = []
    for i in xrange(limit):
        photo = response[i].get('photos', None)
        if photo:
            photos += [photo[0]['original_size']['url']]
    return photos

def get_captions(limit = 1):
    return [james(limit = limit)['response'][i].get('caption', None) for i in xrange(limit)]

if __name__ == '__main__':
    print dumps(james(limit=1), sort_keys=True, indent=4)
    print 'PHOTOS'
    for i, photo in enumerate(get_photos(limit = 10)):
        print i+1, photo
    print 'CAPTIONS'
    for i, caption in enumerate(get_captions(limit = 10)):
        print i+1, caption
