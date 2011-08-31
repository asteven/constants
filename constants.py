import types

__version__ = '0.1.0'

class ConstantsException(Exception):
    pass

class Constants(object):
    def __init__(self, *args, **kwargs):
        self.__offset = kwargs.pop('offset', 0)
        self.__names = []
        self.__values = []
        self.__lookup = {}
        if args:
            for item in args:
                self.__additem(item)
        if kwargs:
            for item in kwargs.items():
                self.__additem(item)

    def __additem(self, item):
        if isinstance(item, ConstantValue):
            name, value, label = str(item), int(item), item.label
        elif isinstance(item, tuple):
            if len(item) == 3:
                name, value, label = item
            else:
                name, value = item
                label = name
        else:
            name = label = item
            if len(self.__values) > 0:
                value = self.__values[-1] + 1
            else:
                value = self.__offset

        if not isinstance(name, (str, unicode)):
            raise ConstantsException, 'constant name is not a string: %s' % name
        if not isinstance(value, int):
            raise ConstantsException, 'constant value is not an integer: %s' % value
        if name in self.__names or name.upper() in self.__names:
            raise ConstantsException, 'constant name is not unique: %s, %s' % (name, name.upper())
        if value in self.__values:
            raise ConstantsException, 'constant value is not unique for %s' % value

        val = ConstantValue(self, name, value, label)
        setattr(self, name, val)
        # ignore case for constant names
        setattr(self, name.upper(), val)
        self.__names.append(name)
        self.__values.append(value)
        self.__lookup[name] = val
        self.__lookup[value] = val

    def __str__(self):
        return 'constants (%s)' % ', '.join(tuple(self.__names))

    def __repr__(self):
        return 'Constants(%s)' % ', '.join(
           [repr(getattr(self, key, None)) for key in self.__names]
        )

    def __iter__(self):
        for key in self.__names:
            yield getattr(self, key, None)

    def __len__(self):
        return len(self.__names)

    def __getitem__(self, item):
        try:
            item = int(item)
        except (ValueError, TypeError):
            pass
        return self.__lookup[item]

    def __add__(self, other):
        return self.__class__(*self.constants() + other.constants())

    def first(self):
        return self.__lookup[self.__names[0]]

    def choices(self):
        items = []
        for key in self.__names:
            item = getattr(self, key, None)
            items.append((int(item), item.label))
        return tuple(items)

    def items(self):
        items = []
        for key in self.__names:
            item = getattr(self, key, None)
            items.append((str(item), int(item)))
        return items

    def constants(self):
        constants = []
        for key in self.__names:
            item = getattr(self, key, None)
            constants.append((str(item), int(item), item.label))
        return constants

    def keys(self):
        return self.__names

    def values(self):
        return self.__values

    def extend(self, *items):
        for name in items:
            self.__additem(name)


class ConstantValue(object):
    def __init__(self, constant, name, value, label):
        self.__constant = constant
        self.__name = name
        self.__value = value
        self.label = label

    def __str__(self):
        return self.__name
    def __int__(self):
        return self.__value
    def __repr__(self):
        return 'ConstantValue(%s, %d)' % (self.__name, self.__value)
    def __cmp__(self, other):
        if isinstance(other, ConstantValue):
             #import sys
             #print >>sys.stdout, 'compare by instance:', other, self
             #sys.stdout.flush()
             #assert self.__constant is other.__constant, "Only values from the same Constants class are comparable"
             return cmp(self.__value, other.__value)
        else:
             return cmp(self.__value, other)


