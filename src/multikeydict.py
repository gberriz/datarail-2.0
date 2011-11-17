from collections import defaultdict
from copy import deepcopy

from pdb import set_trace as ST

class MultiKeyDict(defaultdict):
    '''
    Class to implement nested dictionaries of arbitrary depth.

    This class is most useful (over simply using tuples as keys) when
    there are opportunities for saving time by caching
    sub-dictionaries, especially when the composite keys are
    manipulated programmatically.  In contrast, interactive use of
    this class (as in the illustrative examples below) is expected to
    be cumbersome.

    Examples:
    >>> d = MultiKeyDict()
    >>> d.set((1, 2, 3, 4), "x")
    >>> d.get((1, 2, 3, 4))
    'x'
    >>> d.get((1, 2, 3))
    defaultdict(<class 'multikeydict.MultiKeyDict'>, {4: 'x'})
    >>> d.set((1, 2, 3, 4), "y")
    >>> d.get((1, 2, 3, 4))
    'y'
    >>> d.set((1, 2, 3, 40), "z")
    >>> d.get((1, 2, 3, 40))
    'z'

    Some assignments that implicitly would lead to the deletion of
    subtrees are vetoed.  The user must explicitly delete any subtree
    (e.g. using the delete or popmk method) before carrying out the
    assignment.

    >>> d = MultiKeyDict()
    >>> d.set((1, 2, 3, 4), "x")
    >>> d.set((1,), 5)
    Traceback (most recent call last):
    ...
    TypeError: invalid multikey (must first delete item for multikey [1])
    >>> d.set((1, 2, 3, 4, 5, 6, 7), 8)
    Traceback (most recent call last):
    ...
    TypeError: invalid multikey (must first delete item for multikey [1, 2, 3, 4])
    >>> d.delete((1, 2, 3, 4))
    >>> d.set((1, 2, 3, 4, 5, 6, 7), 8)
    '''

    def __init__(self, maxdepth=None, leafclass=None):
        md = maxdepth
        lc = leafclass
        cls = type(self)

        if md is None:
            assert lc is None
            t = cls
        else:
            if lc is None:
                lc = dict
            assert md > 0
            t = lc if md == 1 else lambda: cls(maxdepth=md - 1, leafclass=lc)

        super(MultiKeyDict, self).__init__(t)

        self.maxdepth = md

    def __getitem__(self, key):
        md = self.maxdepth
        if md is None or md > 1:
            return super(MultiKeyDict, self).__getitem__(key)
        else:
            return dict.__getitem__(self, key)


    def has_key(self, *keys):
        l = self._chkkeys(keys)
        yn = super(MultiKeyDict, self).has_key(keys[0])
        if l == 1 or not yn:
            return yn
        else:
            v = self.__getitem__(keys[0])
            return v.has_key(*keys[1:])

    def _chkkeys(self, keys):
        l = len(keys)
        assert l and hasattr(keys, '__iter__')
        md = self.maxdepth
        if md is not None and l > md:
            raise KeyError('%s (exceeds maxdepth=%d)' % (str(keys), md))
        return l


    def get(self, keys):
        l = self._chkkeys(keys)
        return self._get(keys, l)


    def _get(self, keys, l):
        #v = super(MultiKeyDict, self).__getitem__(keys[0])
        v = self.__getitem__(keys[0])
        return v if l == 1 else v._get(keys[1:], l - 1)


    _OK = object()
    def set(self, keys, val):
        l = self._chkkeys(keys)
        retval = error = None
        try:
            retval = self._set(l - 1, val, keys[0], *keys[1:])
        except Exception, e:
            error = str(e)

        if retval is not MultiKeyDict._OK:
            msg = 'invalid multikey'
            if error is not None:
                msg += ' (%s)' % error
            if hasattr(retval, '__iter__'):
                msg += (' (must first delete item for multikey [%s])'
                        % ', '.join(map(repr, retval)))
            raise TypeError(msg)

    def _set(self, l, val, key, *subkeys):
        hk = self.has_key(key)
        if hk or l > 0:
            v = self.__getitem__(key)
            if hk and ((l == 0) == isinstance(v, MultiKeyDict)):
                return (key,)

        if l == 0:
            super(MultiKeyDict, self).__setitem__(key, val)
        else:
            stat = v._set(l - 1, val, subkeys[0], *subkeys[1:])
            if stat is not MultiKeyDict._OK:
                return (key,) + stat

        return MultiKeyDict._OK

    @staticmethod
    def __todict(value):
        return (value.todict() if hasattr(value, 'todict') else value)

    def todict(self):
        return dict(zip(self.keys(),
                        map(MultiKeyDict.__todict, self.values())))

    @classmethod
    def fromdict(cls, dict_, deep=False):
        ret = cls()
        for k, v in dict_.items():
            ret[k] = (cls.fromdict(v, deep) if isinstance(v, dict)
                      else deepcopy(v) if deep else v)
        return ret
        
    def __str__(self):
        return self.todict().__str__()

    def update(self, dict_):
        for k, v in dict_.items():
            if self.has_key(k):
                vv = self[k]
                if isinstance(vv, MultiKeyDict):
                    if isinstance(v, dict):
                        vv.update(v)
                    else:
                        self.set((k,), vv)
                continue
            self[k] = v

    def delete(self, keys):
        self.popmk(keys)

    def popmk(self, keys):
        l = self._chkkeys(keys)
        try:
            return self._pop(keys, l)
        except KeyError:
            raise KeyError(str(keys))


    def _pop(self, keys, l):
        k = keys[0]
        if not super(MultiKeyDict, self).has_key(k):
            raise KeyError
        if l > 1:
            d = self.__getitem__(k)
            if not isinstance(d, MultiKeyDict):
                raise KeyError
            ret = d._pop(keys[1:], l - 1)
            if not d.keys():
                self.pop(k)
            return ret
        return self.pop(k)