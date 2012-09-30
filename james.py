from urllib2 import urlopen
from json import load, dumps
import re

def james(limit = 1, tag = 'lemon'):
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(response, limit = 1):
    limit = min([len(response), limit])
    photos = [None]*limit
    for i in xrange(limit):
        photo = response[i].get('photos', None)
        if photo:
            photos[i] = photo[0]['original_size']['url']
    return clean(photos)

def get_captions(response, limit = 1):
    limit = min([len(response), limit])
    captions = [response[i].get('caption', None) for i in xrange(limit)]
    return clean(captions)

def clean(a):
    ''' returns same list without empty elements '''
    return [x for x in a if x]

def make_html(photos, captions):
    f = open('index.html', 'w')
    f.write('<html><body>\n')
    for caption in captions:
        f.write(caption + '\n')
    for photo in photos:
        f.write('<img src="{}" width=200 height=100>\n<br \>'.format(photo))
    f.write('</body></html>')
    f.close()

if __name__ == '__main__':
    response = james(limit=10, tag='lemon')['response']
    print dumps(response[0], sort_keys=True, indent=4)
    print 'PHOTOS'
    photos = get_photos(response, limit=10)
    captions = get_captions(response, limit=10)
    for i, photo in enumerate(photos):
        print i+1, photo
    print 'CAPTIONS'
    for i, caption in enumerate(captions):
        for i, caption in enumerate(captions):
        caption = re.sub('<.*?>','',caption)
        print i+1, caption

    make_html(photos, captions)


