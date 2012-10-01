# -*- coding: utf-8 -*-

from urllib2 import urlopen
from json import load, dumps
import re

def james(limit = 1, tag = 'james'):
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(response, limit=10):
    n = len(response)
    photos = [None]*n
    for i in xrange(n):
        photo = response[i].get('photos', None)
        if photo:
            photos[i] = photo[0]['original_size']['url']
    #return clean(photos)[:limit]
    photos = clean(photos)[:limit]
    for i, photo in enumerate(photos):
        img = urlopen(photo).read()
        print photo
        extension = re.search('\.[^\.]*$',photo).group(0)
        open('tmp/%d'%i + extension, 'wb').write(img)
    return ['tmp/%d'%i + extension for i in xrange(limit)]

def get_captions(response, limit=10):
    captions = [r.get('caption', None) for r in response]
    return clean(captions)[:limit]

def clean(a):
    ''' returns same list without empty elements '''
    return [x for x in a if x]

if __name__ == '__main__':
    response = james(limit=20, tag='tiger')['response']
    #print dumps(response[0], sort_keys=True, indent=4)
    print 'PHOTOS'
    photos = get_photos(response)
    captions = get_captions(response)
    for i, photo in enumerate(photos):
        print i+1, photo
    print 'CAPTIONS'
    for i, caption in enumerate(captions):
        print i+1, caption
    #make_html(photos, captions)

def make_html(photos, captions):
    f = open('index.html', 'w')
    f.write('<html><body>\n')
    for caption in captions:
        f.write(caption + '\n')
    for photo in photos:
        f.write('<img src="{}" width=200 height=100>\n<br \>'.format(photo))
    f.write('</body></html>')
    f.close()
