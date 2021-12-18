import re
from urllib.request import urlopen
from json import load, dumps
from multiprocessing import Pool

class TumblrError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_data(url):
    ''' used by parallel crap in get_photos. given a url to a photo, determine
    the extension and read in the binary data. the way multiprocessing works,
    this cannot be a nested function. dumb '''
    data = urlopen(url).read()
    extension = re.search('\.[^\.]*$', url).group(0)
    return extension, data

def james(limit = 1, tag = 'james'):
    ''' return json response from tumblr api '''
    tag = tag.replace(' ', '_')
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&filter=text&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(response, limit=10):
    ''' given json response from call to james function, download 'limit' photos
    with maximum height max_height. saves them into directory 'tmp' with names
    0,1,2,...,limit-1 and same extension. returns list of file names '''
    max_height = 400
    n = len(response)
    print("{} responses from tumblr".format(n))
    urls, photos = [None]*n, [None]*limit
    for i, r in enumerate(response):            # loop through each post
        if 'photos' not in r: continue          # ignore posts without photos
        z = r['photos'][0]                      # dictionary for first photo
        height = z['original_size']['height']
        url = z['original_size']['url']
        if url[-3:] in {'gif', 'GIF'}: continue # latex can't handle gifs
        j, j_max = 0, len(z['alt_sizes'])       # loop through alt sizes 
        while height > max_height:                   # until small enough
            height = z['alt_sizes'][j]['height']
            url = z['alt_sizes'][j]['url']
            j += 1
            if j >= j_max: break
        urls[i] = url
    urls = clean(urls)[:limit]
    print("{} clean urls from tumblr".format(len(urls)))
    if len(urls) < limit:
        raise TumblrError('Too few photos on tumblr.')
    # parallel crap
    pool = Pool(processes=limit)
    pairs = pool.map_async(get_data, urls).get(timeout=5)
    pool.close()
    pool.join()
    for i, p in enumerate(pairs):
        extension, data = p
        photos[i] = 'tmp/%d'%i + extension 
        f = open(photos[i], 'wb').write(data)
    # sequential crap
    #for i, url in enumerate(urls):
    #    data = urlopen(url).read()
    #    extension = re.search('\.[^\.]*$', url).group(0)
    #    photos[i] = 'tmp/%d'%i + extension
    #    open(photos[i], 'wb').write(data)
    return photos

def get_captions(response, tag, limit=10):
    captions = [r.get('caption', None) for r in response]
    captions = clean(captions)[:limit]
    while len(captions) < limit: # default caption if not enough
        captions += [tag] 
    # break at non-alphanumeric between 40 and 80 characters
    for i, c in enumerate(captions):
        c2 = ''
        for word in c.split():
            if len(c2) + len(word) > 80: break
            c2 += word + ' '
            if len(c2) >= 40 and re.search('\W', word): break
        captions[i] = c2
    if len(captions) < limit:
        raise TumblrError('Too few captions on tumblr.')
    captions = [str(caption) for caption in captions]
    return captions

def clean(a):
    ''' returns same list without empty elements '''
    return [x for x in a if x]

if __name__ == '__main__':
    subject = input('topic: ')
    response = james(limit=50, tag=subject)['response']
    #print dumps(response[:5], sort_keys=True, indent=4)
    print('PHOTOS')
    photos = get_photos(response)
    captions = get_captions(response, subject)
    for i, photo in enumerate(photos):
        print(i+1, photo)
    print('CAPTIONS')
    for i, caption in enumerate(captions):
        print(i+1, caption)
