# -*- coding: utf-8 -*-

import sys
import twitter
import couchdb
from couchdb.design import ViewDefinition

SEARCH_TERM = sys.argv[1]
MAX_PAGES = 15
KW = {
    'domain': 'search.twitter.com',
    'count': 200,
    'rpp': 100,
    'q': SEARCH_TERM,
    }
server = couchdb.Server('http://localhost:5984')
DB = 'search-%s' % (SEARCH_TERM.lower().replace('#', '').replace('@', ''), )

try:
    db = server.create(DB)
except couchdb.http.PreconditionFailed, e:

    # already exists, so append to it, keeping in mind that duplicates could occur

    db = server[DB]

# error handling omitted for simplicity

t = twitter.Twitter(domain='search.twitter.com')

for page in range(1, 16):
    KW['page'] = page
    tweets = t.search(**KW)
    db.update(tweets['results'], all_or_nothing=True)
    if len(tweets['results']) == 0:
        break
    print 'Fetched %i tweets' % len(tweets['results'])
