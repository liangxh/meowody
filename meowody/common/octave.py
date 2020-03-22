class Octave(object):
    UP = '\''
    DOWN = '.'
    mark_to_value = {UP: 1, DOWN: -1}

    @classmethod
    def to_str(cls, v):
        if v == 0:
            return ''
        elif v > 0:
            return cls.UP * v
        else:
            return cls.DOWN * (-v)

    @classmethod
    def loads(cls, s):
        if s is None or len(s) == 0:
            return 0
        else:
            return cls.mark_to_value[s[0]] * len(s)
