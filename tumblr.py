import re
from urllib2 import urlopen
from json import load, dumps
from multiprocessing import Pool

def get_data(url):
    data = urlopen(url).read()
    extension = re.search('\.[^\.]*$', url).group(0)
    return extension, data

def james(limit = 1, tag = 'james'):
    tag = tag.replace(' ', '_')
    key = 'XO7suEuSmJhFAZdhHJBjDYeaecyfVatJBKtOhFzG8AH0VTiArJ' # consumer key
    url = 'http://api.tumblr.com/v2/tagged?tag=%s&limit=%d&filter=text&api_key=%s'
    return load(urlopen(url % (tag, limit, key)))

def get_photos(response, limit=10):
    max_height = 400
    n = len(response)
    urls, photos = [None]*n, [None]*limit
    for i, r in enumerate(response):
        if 'photos' not in r: continue
        z = r['photos'][0]
        h = z['original_size']['height']
        url = z['original_size']['url']
        if url[-3:] in {'gif', 'GIF'}: continue
        j, j_max = 0, len(z['alt_sizes'])
        while h > max_height:
            h = z['alt_sizes'][j]['height']
            url = z['alt_sizes'][j]['url']
            j += 1
            if j >= j_max: break
        urls[i] = url
    urls = clean(urls)[:limit]
    pool = Pool(processes=limit)
    pairs = pool.map_async(get_data, urls).get(timeout=5)
    for i, p in enumerate(pairs):
        extension, data = p
        photos[i] = 'tmp/%d'%i + extension 
        f = open(photos[i], 'wb').write(data)
    #for i, url in enumerate(urls):
    #    data = urlopen(url).read()
    #    extension = re.search('\.[^\.]*$', url).group(0)
    #    photos[i] = 'tmp/%d'%i + extension
    #    open(photos[i], 'wb').write(data)
    return photos

def get_captions(response, limit=10):
    captions = [r.get('caption', None) for r in response]
    captions = clean(captions)[:limit]
    while len(captions) < limit:
        captions += ['james']
    captions = [re.sub(r'\s+', ' ', c)[:80] for c in captions]
    return captions

def clean(a):
    ''' returns same list without empty elements '''
    return [x for x in a if x]

if __name__ == '__main__':
    subject = raw_input('topic: ')
    response = james(limit=20, tag=subject)['response']
    #print dumps(response[:5], sort_keys=True, indent=4)
    print 'PHOTOS'
    photos = get_photos(response)
    captions = get_captions(response)
    for i, photo in enumerate(photos):
        print i+1, photo
    print 'CAPTIONS'
    for i, caption in enumerate(captions):
        print i+1, caption
