from urllib2 import urlopen
from json import load, dumps
import re

def james(limit = 1, tag = 'james'):
    tag = tag.replace(' ', '_')
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&filter=text&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(response, limit=10):
    n = len(response)
    urls, photos = [None]*n, [None]*limit
    for i in xrange(n):
        url = response[i].get('photos', None)
        if url:
            urls[i] = url[0]['original_size']['url']
    urls = clean(urls)
    i = 0
    for url in urls:
        data = urlopen(url).read()
        print url
        extension = re.search('\.[^\.]*$', url).group(0)
        if extension in {'.gif', '.GIF'}: 
            continue
        photos[i] = 'tmp/%d'%i + extension
        open(photos[i], 'wb').write(data)
        i += 1
        if i >= limit: break
    return photos

def get_captions(response, limit=10):
    captions = [r.get('caption', None) for r in response]
    captions = clean(captions)[:limit]
    while len(captions) < limit:
        captions += ['james']
    return captions

def clean(a):
    ''' returns same list without empty elements '''
    return [x for x in a if x]

if __name__ == '__main__':
    subject = raw_input('topic: ')
    response = james(limit=20, tag=subject)['response']
    #print dumps(response[0], sort_keys=True, indent=4)
    print 'PHOTOS'
    photos = get_photos(response)
    captions = get_captions(response)
    for i, photo in enumerate(photos):
        print i+1, photo
    print 'CAPTIONS'
    for i, caption in enumerate(captions):
        print i+1, caption
