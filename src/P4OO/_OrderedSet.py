''' OrderedSet

Copied from http://code.activestate.com/recipes/576694/

Created by Raymond Hettinger
Licensed under the MIT License

Modified by David L. Armstrong to avoid use of 'next' keyword
and add indexing support
'''

import collections.abc

KEY, PREV, NEXT = range(3)

class OrderedSet(collections.abc.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[PREV]
            curr[NEXT] = end[PREV] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prevItem, nextItem = self.map.pop(key)
            prevItem[NEXT] = nextItem
            nextItem[PREV] = prevItem

    # indexing support
    def __getitem__(self, key):
        if not isinstance(key, int):
            raise KeyError(key)

        if key >= len(self) or key < (len(self) * -1):
            raise KeyError(key)

        counter = 0
        if key >= 0:
            item = self.end
            while counter <= key:
                item = item[NEXT]
                counter += 1
            return item[KEY]
        else:
            item = self.end
            while counter > key:   # > because 0 is the start, not 1
                item = item[PREV]
                counter -= 1
            return item[KEY]

        # catchall
        raise KeyError(key)


    def __iter__(self):
        end = self.end
        curr = end[NEXT]
        while curr is not end:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self):
        end = self.end
        curr = end[PREV]
        while curr is not end:
            yield curr[KEY]
            curr = curr[PREV]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = next(reversed(self)) if last else next(iter(self))
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __del__(self):
        self.clear()                    # remove circular references
