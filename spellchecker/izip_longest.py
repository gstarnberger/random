# This is directly copied from
# http://docs.python.org/library/itertools.html#itertools.izip_longest

# My code uses itertools.izip_longest which is included in Python since version
# 2.6, but according to given specs the code should run on Python 2.5. If the
# code is executed on Python < 2.6 the izip_longest implementation within this
# module is used.

from itertools import chain, izip, repeat

def izip_longest(*args, **kwds):
    fillvalue = kwds.get('fillvalue')
    def sentinel(counter = ([fillvalue]*(len(args)-1)).pop):
        yield counter()
    fillers = repeat(fillvalue)
    iters = [chain(it, sentinel(), fillers) for it in args]
    try:
        for tup in izip(*iters):
            yield tup
    except IndexError:
        pass
