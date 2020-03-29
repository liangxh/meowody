class Accidental(object):
    """
    变音号
    """
    SHARP = 1
    DOUBLE_SHARP = 2
    FLAT = -1
    DOUBLE_FLAT = -2
    NONE = 0

    @classmethod
    def loads(cls, s):
        return {'b': cls.FLAT, '#': cls.SHARP, 'bb': cls.DOUBLE_FLAT, None: cls.NONE}[s]

    @classmethod
    def symbol(cls, v):
        return {cls.FLAT: 'b', cls.SHARP: '#', cls.DOUBLE_FLAT: 'bb', cls.NONE: ''}[v]
