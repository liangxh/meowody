class Duration(object):
    t_1 = '0'
    t_2 = 'a'
    t_4 = 'x'
    t_8 = '-'
    t_16 = '='

    str_to_t = {t_1: 1, t_2: 2, t_4: 4, t_8: 8, t_16: 16}

    def __init__(self, t, add_half=False):
        self.t = t
        self.add_half = add_half
        if not add_half:
            self.a = 1
            self.b = t
        else:
            self.a = 3
            self.b = t * 2

    @classmethod
    def loads(cls, v):
        add_half = False
        if v.endswith('.'):
            add_half = True
            v = v[:-1]
        t = cls.str_to_t[v]
        return cls(t, add_half)

    def get_scale(self):
        return self.b

    def get_print_len(self, scale):
        _a = scale * self.a
        if _a % self.b != 0:
            raise Exception('scale mismatch! scale={}, duration={}/{}', scale, self.a, self.b)
        return _a // self.b
