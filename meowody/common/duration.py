import re


class Duration(object):
    t_1 = 'o'
    t_2 = 'e'
    t_4 = 'x'
    t_8 = '-'
    t_16 = '='

    str_to_t = {t_1: 1, t_2: 2, t_4: 4, t_8: 8, t_16: 16}
    _str_pattern = re.compile('^([^.]*)(.*)$')

    def __init__(self, t, add_half=0):
        self.t = t
        self.add_half = add_half
        if add_half == 0:
            self.a = 1
            self.b = t
        else:
            _multiplier = 2 ** add_half
            self.a = 2 * _multiplier - 1
            self.b = t * _multiplier

    @classmethod
    def loads(cls, v):
        res = cls._str_pattern.match(v)
        if res is None:
            raise Exception('failed to load as duration: {}'.format(v))
        t_mark, half_mark = res.groups()
        t = cls.str_to_t[t_mark]
        add_half = len(half_mark) if half_mark is not None else 0
        return cls(t, add_half)

    def get_scale(self):
        return self.b

    def get_print_len(self, scale):
        _a = scale * self.a
        if _a % self.b != 0:
            raise Exception('scale mismatch! scale={}, duration={}/{}', scale, self.a, self.b)
        return _a // self.b
